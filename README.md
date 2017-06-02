# Why pybibs?

I needed to evince a minimal knowledge of d3.js for self-marketing purposes, so I wrote this simple script over a weekend. 

But seriously:

You manage your references using Bibtex. You have multiple .bib files around and you also like to use the keyword field in most entries in your bibliography. Wouldn't it be nice to be able to get some basic counts on your citation for a particular keyword? Or maybe you'd like to create a .bib file for each keyword for future re-use?

Pybibs does just that: https://raresct.github.io/pybibs/

Hovering over a bar in the bar chart shows the actual citation count and clicking a bar shows only entries having the corresponding keyword (the .bib file and the .html file are naively pre-generated). 

# Dependencies

Python:

* numpy
* matplotlib
* lxml
* requests
* python-fire (https://github.com/google/python-fire)

Unix:

* bibtool
* bibtex2html


# Usage

`$ python pybibs.py run --files=FILE1,FILE2,...`

e.g. the example above is created by

`$ python pybibs.py run --files=test/plp15.bib,test/plp15_copy.bib`

The final output will be stored in index.html. To view it, use:

`$ python -m SimpleHTTPServer`

, then open localhost:8000 in your favorite browser.

# License

MIT

Copyright 2017 Calin Rares Turliuc

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
