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

from nti.contenttools.renderers.model import DefaultRendererContext

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


def render_document(document, context):
    context.write(document_class(document.doc_type))
    for package in document.packages or ():
        context.write(use_package(package))
    if document.title:
        context.write(document_title(document.title))
    if document.author:
        context.write(document_title(document.author))
    for child in document.children or ():
        renderer = component.getAdapter(child, 
                                        IRenderer, 
                                        name=context.name)
        renderer.render(context, child)


@component.adapter(IDocument)
@interface.implementer(IRenderer)
class DocumentRenderer(object):

    __slots__ = ('document',)

    def __init__(self, document):
        self.document = document

    def render(self, context=None, node=None):
        document = self.document if node is None else node
        context = DefaultRendererContext() if context is None else None
        context.write(document_class(document.doc_type))
        for package in document.packages or ():
            context.write(use_package(package))
        if document.title:
            context.write(document_title(document.title))
        if document.author:
            context.write(document_author(document.author))
    __call__ = render
