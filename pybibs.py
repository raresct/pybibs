# coding=utf-8
#!/usr/bin/env python2

'''

Non-Python Dependencies:
- bibtool
    > URL: https://github.com/ge-ne/bibtool)
    > version: $bibtool -V
                BibTool Vers. 2.62-alpha (C) 1996-2015 Gerd Neugebauer

                Library path: .:/usr/local/lib/BibTool
                Special configuration options: none
- bibtex2html
    > URL: https://github.com/backtracking/bibtex2html
    > version: $bibtex2html -v
                This is bibtex2html version 1.98, compiled on Sun Jul 6 23:12:51 UTC 2014
                Copyright (c) 1997-2010 Jean-Christophe Filliâtre and Claude Marché
                This is free software with ABSOLUTELY NO WARRANTY (use option --warranty)

'''

import os
import sys
import lxml.html
import requests
import re
import math
import cStringIO
import subprocess
import shlex
import shutil
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter

import fire

def rewrite_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)

def call_cmd(cmd_str, outf=None):
    devnull = open('/dev/null', 'w')
    if not outf:
        outf = devnull
    p1 = subprocess.Popen(shlex.split(cmd_str),
        stdout=outf, stderr=devnull)
    p1.wait()


class PyBibs(object):
    def run(self, files):
        rewrite_dir('key_htmls')

        # IN
        # bib_files = ['test/plp15.bib', 'test/plp15_copy.bib']
        bib_files = [i.strip() for i in files.split(',')]

        outf = 'all_bibs.bib'
        outhtml = 'all_bibs.html'
        outhtml1 = 'all_bibs_tagged.html'
        keystr = 'Keywords: '
        key_count = Counter()

        all_bibs = ' '.join(bib_files)
        call_cmd('bibtool -s -d {}'.format(all_bibs), open(outf, 'w'))
        call_cmd('bibtex2html {}'.format(outf), open('log', 'w'))

        dom = lxml.html.fromstring(open(outhtml,'r').read())
        key_els = dom.xpath('.//td[@class="bibtexitem"]/blockquote[contains(.,"Keywords:")]')

        keyw_ref_ids = {}
        for key_el in key_els:
            key_names = ([s.strip()
                for s in ' '.join(key_el.text_content().strip().split())
                    [len(keystr):].split(",")])
            key_strs = [k.replace(' ', '_') for k in key_names]
            key_count.update(key_strs)
            for sub_el in key_el:
                key_el.remove(sub_el)
            key_el.append(lxml.html.fromstring('<span>{}</span>'.format(keystr)))
            ref_id = key_el.getparent().getparent()[0][0].get('name')
            for s,name in zip(key_strs,key_names):
                key_el.append(lxml.html.fromstring(
                '<span class="outline rcorner {}"><a href="{}">{}</a></span>'
                .format(s,'key_htmls/{}.html'.format(s),name)))
                if keyw_ref_ids.has_key(s):
                    keyw_ref_ids[s].append(ref_id)
                else:
                    keyw_ref_ids[s] = [ref_id]
        lxml.etree.ElementTree(dom).write(outhtml1, pretty_print=True)

        '''
        with open(outhtml, 'r') as f, open(outhtml1, 'w') as fout:
            for line in f:
                if line.startswith(keystr):
                    key_names = [s.strip() for s in line.strip()[len(keystr):].split(",")]
                    key_strs = [k.replace(' ', '_') for k in key_names]
                    key_count.update(key_strs)
                    out_line = keystr+','.join([
                        '<span class="outline rcorner {}"><a href="{}">{}</a></span>'
                        .format(s,'key_htmls/{}.html'.format(s),name)
                        for s,name in zip(key_strs,key_names)])+'\n'
                    fout.write(out_line)
                else:
                    fout.write(line)
        '''

        print key_count

        labels, values = zip(*key_count.most_common())
        indexes = np.arange(len(labels))
        width = 1

        cmap = plt.cm.get_cmap('nipy_spectral')
        colors = [cmap(x) for x in np.linspace(0,1,len(labels))]

        def get_upscaled_value(colors):
            """
            Scales an RGB color object from decimal 0.0-1.0 to int 0-255.
            """
            new_colors = []
            for color in colors:
                # Scale up to 0-255 values.
                r = int(math.floor(0.5 + color[0] * 255))
                g = int(math.floor(0.5 + color[1] * 255))
                b = int(math.floor(0.5 + color[2] * 255))
                new_colors.append([r,g,b])
            return new_colors

        colors = get_upscaled_value(colors)

        with open('data.csv', 'w') as f:
            f.write(','.join(['label', 'value', 'r','g','b', 'url'])+'\n')
            for label, value, color in zip(labels, values, colors):
                f.write(','.join([label.replace('_', ' '), str(value), str(color[0]),
                    str(color[1]), str(color[2]), 'key_htmls/{}.html'.format(label)])
                    +'\n')

        '''
        plt.figure(figsize=(8,len(labels)/3))
        plt.barh(indexes, values, width, color=colors)
        plt.yticks(indexes + width * 0.5, labels)
        ax = plt.gca()
        ax.xaxis.grid(True)


        format = "png"
        sio = cStringIO.StringIO()
        plt.savefig(sio, format=format)
        with open('test.html', 'w') as f:
            f.write("""<html><body>
        ...a bunch of text and html here...
        <img src="data:image/png;base64,{}"/>
        ...more text and html...
        </body></html>""".format(sio.getvalue().encode("base64").strip()))
        '''

        css = '''
        <style>
        .outline {{
            padding: 3px;
        }}

        .rcorner {{
            border-radius: 5px;
        }}

        span.rcorner a {{
            text-decoration: none;
            color: inherit;
        }}

        span.outline a {{
            color: white;
            font-size: 12pt;
            font-family:arial;
            text-shadow:
            1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000,
            -1px 1px 0 #000, 0px 0px 0px #000;
            /*
            -webkit-text-stroke: 0.4px black;
            -webkit-text-fill-color: white;
            */
        }}

        {}

        </style>
        '''.format('\n'.join(['''
        .{} {{
            background-color: rgb({},{},{});
        }}'''.format(label, color[0], color[1], color[2])
            for label,color in zip(labels, colors)]))

        print('Data written to csv. Now writing index.html.')

        css_el = lxml.html.fromstring(css).find('.//style')
        d3_el = lxml.html.fromstring(open('d3.txt','r').read()).find('.//script')
        d3_import_el = lxml.html.fromstring(
            '<script src="https://d3js.org/d3.v3.min.js"></script>').find('.//script')
        h1 = lxml.html.fromstring(
            '<div> <hr> <h1>References</h1> </div>')

        dom = lxml.html.fromstring(open(outhtml1,'r').read())
        head = dom.find('.//head')
        head.append(css_el)
        head.append(d3_import_el)
        body = dom.find('.//body')
        body.insert(0, d3_el)
        body.insert(1, h1)
        body.append(lxml.html.fromstring(
            '<p><em>Bar chart and keyword style by pybibs.</em></p>'))
        with open('index.html', 'w') as f:
            f.write(lxml.html.tostring(dom))

        print('Index.html written. Now creating bibs for each keyword.')

        # create bibs for each keyword
        for k,v in keyw_ref_ids.items():
            k_name = k
            k = k.replace(' ', '_')
            key_f = 'key_htmls/{}.bib'.format(k)
            key_html = 'key_htmls/{}.html'.format(k)
            with open(key_f, 'w') as f:
                f.write(' '.join(v))
            call_cmd('bibtex2html -citefile {} -o - {}'.format(key_f, outf), open(key_html, 'w'))
            dom = lxml.html.fromstring(open(key_html,'r').read())
            body = dom.find('.//body')
            h1 = lxml.html.fromstring(
            '<div> <a href="../index.html">Back</a> <h1>References for "{}"</h1> </div>'.format(k_name))
            body.insert(0, h1)
            with open(key_html, 'w') as f:
                f.write(lxml.html.tostring(dom))

        print('Done.')

if __name__=='__main__':
    fire.Fire(PyBibs)
