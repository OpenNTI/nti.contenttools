#!/usr/bin/env python2.7

import math
import os
import re
import sys


def _parse_csv(data):
    result = {}

    for line in data.readlines():
        _t = line.split(',')
        if _t[0] not in result:
            result[_t[0]] = []
        result[_t[0]].extend([_t[1]])

    return result;

def _process_lines(lines, r):
    result = []
    
    for line in lines:
        p = re.match(r'\\label{qid\.([1-9][0-9]*)}', line)
        if p is not None:
            if p.group(1) in r:
                for el in r[p.group(1)]:
                    line = line + r'\naqvideo{http://www.youtube.com/embed/' + el.strip() + '?rel=0}{http://img.youtube.com/vi/' + el.strip() + '/default.jpg}\n'

        result.extend([line])

    return result

def main():
    r = {}
    lines = []
    with open( sys.argv[1:][0], 'rb' ) as file:
        print("Reading CSV.")    
        r = _parse_csv(file)

    with open( sys.argv[1:][1], 'rb' ) as file:
        print("Reading source.")
        lines = file.readlines()

    lines = _process_lines(lines, r)

    with open( sys.argv[1:][1], 'wb' ) as file:
        print("Writing altered source.")
        file.write(''.join(lines) )


if __name__ == '__main__':
    main()
