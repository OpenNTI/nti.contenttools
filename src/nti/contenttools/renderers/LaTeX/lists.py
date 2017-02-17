#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: list.py 65711 2015-05-20 21:08:17Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_environment
from nti.contenttools.renderers.LaTeX.base import render_children_output
from nti.contenttools.renderers.LaTeX.base import render_iterable

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IDD
from nti.contenttools.types.interfaces import IDT
from nti.contenttools.types.interfaces import IItem
from nti.contenttools.types.interfaces import IList
from nti.contenttools.types.interfaces import IOrderedList
from nti.contenttools.types.interfaces import IItemWithDesc
from nti.contenttools.types.interfaces import IUnorderedList
from nti.contenttools.types.interfaces import IDescriptionList


def render_unordered_list(context, node):
    return render_environment(context, u'itemize', node)
    


def render_ordered_list(context, node):
    optional = u''
    if node.format == 'decimal':
        optional = u'1'
    elif node.format == 'lowerLetter':
        optional = u'a'
    elif node.format == 'upperLetter':
        optional = u'A'
    elif node.format == 'lowerRoman':
        optional = u'i'
    elif node.format == 'upperRoman':
        optional = u'I'

    if node.start != 1:
        if optional:
            optional = u'%s, start=%s' % (optional, node.start)
        else:
            optional = u'start=%s' % (node.start)

    if optional:
        optional = u'[' + optional + u']'

    check = render_children_output(node)
    if u'\\item' in check:
        return render_environment(context, u'enumerate', node, optional)
    else:
        return check


def render_list(context, node):
    return render_environment(context, u'itemize', node)
    


def render_item(context, node):
    desc = render_children_output(node)
    if u'\\chapter' in desc:
        return desc
    context.write(u'\\item %s \n' % desc)
    return node


def render_description_list(context, node):
    return render_environment(context, u'description', node)


def render_item_with_description(context, node):
    return render_children_output(node)


def render_dt(context, node):
    if node.desc:
        desc = render_children_output(node.desc) 
    else:
        desc = u''
    item = render_children_output(node)
    if node.type_ is None:
        context.write(u'\\item [%s] %s \n' % (item, desc))
    else:
        context.write(u'\\item [%s] \\hfill \\\\\n%s \n' % (item, desc))
    return node


def render_dd(context, node):
    return render_children_output(node)


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(IDD)
class DDRenderer(RendererMixin):
    func = staticmethod(render_dd)


@component.adapter(IDT)
class DTRenderer(RendererMixin):
    func = staticmethod(render_dt)


@component.adapter(IItem)
class ItemRenderer(RendererMixin):
    func = staticmethod(render_item)


@component.adapter(IList)
class ListRenderer(RendererMixin):
    func = staticmethod(render_list)


@component.adapter(IOrderedList)
class OrderedListRenderer(RendererMixin):
    func = staticmethod(render_ordered_list)


@component.adapter(IUnorderedList)
class UnorderedListRenderer(RendererMixin):
    func = staticmethod(render_unordered_list)


@component.adapter(IDescriptionList)
class DescriptionListRenderer(RendererMixin):
    func = staticmethod(render_description_list)


@component.adapter(IItemWithDesc)
class ItemWithDescriptionRenderer(RendererMixin):
    func = staticmethod(render_item_with_description)
