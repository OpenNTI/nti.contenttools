import os
import csv
import codecs
import argparse

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.concept import ConceptHierarchy
from nti.contenttools.types.concept import Concept

from zope.component.hooks import setHooks

from zope.configuration import xmlconfig

import nti.contenttools


def setup_context(context=None):
    context = xmlconfig.file('configure.zcml',
                             package=nti.contenttools,
                             context=context)
    return context


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Parse CSV to LaTex Concepts Tree")
    arg_parser.add_argument('input',
                            help="CSV filepath")
    arg_parser.add_argument('-c', '--column',
                            help="Concept's column",
                            default="Concepts")
    arg_parser.add_argument('-o', '--output',
                            help="LaTex filename",
                            default=None)
    return arg_parser.parse_args()


def write_file(filename, contents):
    with codecs.open(filename, "w") as fp:
        fp.write(contents)


def read_csv(filename, column):
    names = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            names.append(unicode(row[column]))
    return names


def build_concepts_tree(names):
    ctree = ConceptHierarchy()
    for name in names:
        concept = Concept(name=name)
        ctree.add_child(concept)
    return ctree


def main():
    setup_context()
    args = parse_args()
    names = read_csv(args.input, args.column)
    print(names)
    if names:
        ctree = build_concepts_tree(names)
        context = DefaultRendererContext(name=u"LaTeX")
        render_node(context, ctree)
        tex_tree = context.read()
        output = args.output
        if not output:
            dir_path = os.path.split(args.input)[0]
            output = os.path.join(dir_path, 'Concepts.tex')
        write_file(output, tex_tree)


if __name__ == '__main__':  # pragma: no cover
    main()
