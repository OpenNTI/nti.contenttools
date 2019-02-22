import os
import csv
import json
import codecs
import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Create a latex file of glossary toc")
    arg_parser.add_argument('input',
                            help="Directory path where glossary json files are located")
    arg_parser.add_argument('-o', '--output',
                            help="LaTex filename",
                            default=None)
    return arg_parser.parse_args()


def read_list_of_glossary_files(dir_path):
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    glossaries = {}
    for filename in files:
        if u'.json' in filename:
            print(u'Read .. {}'.format(filename))
            glossary = read_json(filename)
            glossaries.update(glossary)
    return glossaries


def read_json(filename):
    try:
        with codecs.open(filename, 'r') as fp:
            data = json.load(fp)
        return data
    except OSError as e:
        print('File {filename} not found'.format(filename))


def write_file(filename, contents):
    with codecs.open(filename, "w", encoding="utf-8") as fp:
        fp.write(contents)


def build_glossary_toc(dir_path):
    glossaries = read_list_of_glossary_files(dir_path)
    glossary_list = []
    for term in sorted(glossaries):
        ref = u'{}<{}>\\\\'.format(glossaries[term], term)
        glossary_list.append(ref)
    return u'\n'.join(glossary_list)


def main():
    args = parse_args()
    toc = build_glossary_toc(args.input)
    output = args.output
    if not output:
        output = os.path.join(args.input, 'glossary_toc.tex')
        write_file(output, toc)


if __name__ == '__main__':  # pragma: no cover
    main()
