#!/usr/bin/env python2.7

import math
import os
import re
import sys

MAX_IMAGE_WIDTH = 450

def beamer_import(data):    
    output = []
    title = ''
    for line in data.readlines():
        line = line.replace('\\tableofcontents', '')
        line = line.replace('\\maketitle', '')
        line = line.replace('\\titlepage', '')
        line = line.replace('\\begin{document}', '')
        line = line.replace('\\end{document}', '')
        line = re.sub('<[A-Za-z0-9]*>','',line)


        #_t = re.search(r'([0-9.]*)(\\linewidth)', line)
        #if _t is not None:
        #    scaler = _t.group(1).strip()
        #    if scaler is '': scaler = '1'
        #    line = line.replace(_t.group(1) + '\\linewidth', str(MAX_IMAGE_WIDTH * float(scaler)) + 'pt')

        _t = re.search(r'textgraphics{([0-9.]*)}', line)
        if _t is not None:
            line = line.replace(_t.group(1), str(MAX_IMAGE_WIDTH * float(_t.group(1))) + 'pt')

        _t = re.search(r'\\includegraphics{*\[*[A-Za-z0-9 \.=_-]*\]*}*{([A-Za-z0-9_.-]*)}', line)
        if _t is not None:
            if '/' not in _t.group(1):
                line = line.replace(_t.group(1), 'graphics/' + _t.group(1))

        output.extend([line])

    return output

if __name__ == '__main__':
    with open( sys.argv[1:][0], 'rb' ) as data:
        output = beamer_import(data)

        for line in output:
            sys.stdout.write(line)
