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
    arg_parser.add_argument('-f', '--figurecount',
                            default=1,
                            help="Count figure as n words. The default is count figure as 1 word")
    arg_parser.add_argument('-t', '--tablecount',
                            default=1,
                            help="Count table as n words. The default is count table as 1 word")
    arg_parser.add_argument('-i', '--nonfigureimage',
                            default=1,
                            help="Count non figure image as n words. The default is count non figure image as 1 word")
    arg_parser.add_argument('-d', '--details',
                            default='false',
                            help="Set true if we want to include image, table, and figure count in total word count. Set false if we do not want to include them. The default is false")
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

def write_to_csv(data_csv, filename, header, details=False):
    try:
        with codecs.open(filename, 'w') as fp:
            w = csv.writer(fp)
            w.writerow(header)
            if not details:
                rows = [(ntiid, 
                         data.title.encode("utf-8"), 
                         data.block, 
                         data.minutes, 
                         data.total_words) 
                for ntiid, data in data_csv.items()]
                w.writerows(rows)
            else:
                rows = [(ntiid, 
                         data.title.encode("utf-8"), 
                         data.block, 
                         data.minutes, 
                         data.total_words, 
                         data.details['figure_count_word'],
                         data.details['table_count_word'],
                         data.details['non_figure_image_word_count']) 
                for ntiid, data in data_csv.items()]
                w.writerows(rows)
    except OSError as e:
        raise e


def output_csv(name):
    FORBIDDEN_CHARACTERS = r'[<>:"/\\\|\?\*\s\-,\t\'\!{}()]'
    value = re.sub(FORBIDDEN_CHARACTERS, '_', name)
    return u'%s.csv' %value

def process_data(data, root, block, wpm, tup, data_csv, details=()):
    if 'ntiid' in root.attrib and 'label' in root.attrib:
        ntiid = root.attrib['ntiid']
        label = root.attrib['label']
        if ntiid in data:
            detail_dict = get_block_element_detail(data[ntiid], details)
            if details:
                total_words = data[ntiid]['total_word_count'] \
                              + sum([detail_dict[key] for key in detail_dict])
            else:
                total_words = data[ntiid]['total_word_count']
            minutes = float(total_words)/float(wpm)
            nblocks = minutes//block
            row = tup(title=label, block=nblocks, minutes=minutes, total_words=total_words, details=detail_dict)
            data_csv[ntiid] = row
    for child in root:
        process_data(data, child, block, wpm, tup, data_csv, details) 

def get_block_element_detail(el, details):
    detail_dict = {}
    if 'figurecount' in details:
        fig_count = el["BlockElementDetails"]['figure']['count']
        detail_dict['figure_count_word'] = fig_count * details['figurecount']

    if 'tablecount' in details:
        table_count = el["BlockElementDetails"]['table']['count']
        detail_dict['table_count_word'] = table_count * details['tablecount']

    if 'nonfigureimage' in details:
        image_count = el["non_figure_image_count"]
        detail_dict["non_figure_image_word_count"] = image_count * details["nonfigureimage"]
    return detail_dict

def build_details(args):
    details= {}
    details['figurecount'] = args.figurecount
    details['tablecount'] = args.tablecount
    details['nonfigureimage'] = args.nonfigureimage
    return details

def main():
    # Parse command line args
    args = parse_args()
    block = args.block
    wpm = args.wpm
    
    xml = os.path.join(args.inputdir, 'eclipse-toc.xml')
    root = read_xml(xml)

    filejson = os.path.join(args.inputdir, 'content_metrics.json')
    data = read_json(filejson)

    tup = namedtuple('tup', ['title', 'block', 'minutes', 'total_words', 'details'])
    data_csv = OrderedDict()

    output = output_csv(root.attrib['label'])
    nblock = u'%smin Blocks' %block

    if args.details in (1, 'true', 'True'):
        args.details = True
    else:
        args.details = False

    if args.details:
        header = ('NTIID', 'Title', nblock, 'Minutes', 'Total words', 'Figures counted as words', 'Tables counted as words', 'Non Figure Image counted as words')
        details = build_details(args)
        process_data(data, root, block, wpm, tup, data_csv, details)
    else:
        header = ('NTIID', 'Title', nblock, 'Minutes', 'Total Words')
        process_data(data, root, block, wpm, tup, data_csv)
    
    write_to_csv(data_csv, output, header, args.details)

if __name__ == '__main__':  # pragma: no cover
    main()