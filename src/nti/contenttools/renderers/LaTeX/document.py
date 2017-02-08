#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.types.interfaces import IBody
from nti.contenttools.types.interfaces import IDocument


def document_class(docclass, options=''):
    if options:
        options = u'[%s]' % options
    return u'\\documentclass%s{%s}\n' % (options, docclass)


def use_package(package, options=''):
    if options:
        options = u'[%s]' % options
    return u'\\usepackage%s{%s}\n' % (options, package)


def document_title(title):
    return u'\\title{%s}\n' % title


def document_author(author):
    return u'\\author{%s}\n' % author


def render_document(context, document):
    context.write(document_class(document.doc_type))
    for package in document.packages or ():
        context.write(use_package(package))
    if document.title:
        context.write(document_title(document.title))
    if document.author:
        context.write(document_author(document.author))
    render_children(context, document)
    return document


def render_body(context, body, optional=''):
    context.write(u'\\begin{document}')
    if optional:
        context.write(optional)
    context.write("\n")
    render_children(context, body)
    context.write(u'\n\\end{document}\n')
    return body


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(IDocument)
class DocumentRenderer(RendererMixin):
    func = staticmethod(render_document)


@component.adapter(IBody)
class BodyRenderer(RendererMixin):
    func = staticmethod(render_body)
