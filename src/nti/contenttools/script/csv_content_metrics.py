#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import argparse
import json
import csv

import xml.etree.ElementTree as ET

from collections import namedtuple, OrderedDict


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Update text files")
    arg_parser.add_argument('inputdir',
                            help="Content package dir")
    arg_parser.add_argument('-w', '--wpm',
                            default=200,
                            help="Average words per minute")
    arg_parser.add_argument('-b', '--block',
                            default=15,
                            help="Minutes block. The default is 15")
    return arg_parser.parse_args()

def read_json(filename):
    try:
        with codecs.open(filename, 'r') as fp:
            data = json.load(fp)
        return data
    except OSError as e:
        print('File {filename} not found'.format(filename))


def read_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        return root
    except Exception, e:
        raise

def write_to_csv(data_csv, filename, header):
    try:
        with codecs.open(filename, 'w') as fp:
            w = csv.writer(fp)
            w.writerow(header)
            w.writerows([(ntiid, data.title, data.block, data.minutes, data.total_words) for ntiid, data in data_csv.items()])
        return data
    except OSError as e:
        raise e


def output_csv(name):
    FORBIDDEN_CHARACTERS = r'[<>:"/\\\|\?\*\s\-,\t\'\!{}()]'
    value = re.sub(FORBIDDEN_CHARACTERS, '_', name)
    return u'%s.csv' %value

def process_data(data, root, block, wpm, tup, data_csv):
    if 'ntiid' in root.attrib and 'label' in root.attrib:
        ntiid = root.attrib['ntiid']
        label = root.attrib['label']
        if ntiid in data:
            total_words = data[ntiid]['total_word_count']
            minutes = float(total_words)/float(wpm)
            nblocks = minutes//block
            row = tup(title=label, block=nblocks, minutes=minutes, total_words=total_words)
            data_csv[ntiid] = row
    for child in root:
        process_data(data, child, block, wpm, tup, data_csv) 


def main():
    # Parse command line args
    args = parse_args()
    block = args.block
    wpm = args.wmp
    
    xml = os.path.join(args.inputdir, 'eclipse-toc.xml')
    root = read_xml(xml)

    filejson = os.path.join(args.inputdir, 'content_metrics.json')
    data = read_json(filejson)

    tup = namedtuple('tup', ['title', 'block', 'minutes', 'total_words'])
    data_csv = OrderedDict()

    process_data(data, root, block, wpm, tup, data_csv)

    output = output_csv(root.attrib['label'])
    write_to_csv(data_csv, output, ('NTIID', 'Title', 'Block', 'Minutes', 'Total Words'))

if __name__ == '__main__':  # pragma: no cover
    main()