#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: chapter_assessment.py 109681 2017-03-27 06:28:00Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.types.interfaces import ICNXProblemSolution

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.renderers.interfaces import IRenderer


def render_cnx_problem_solution(context, node):
    title = get_variant_field_string_value(node.title)
    context.write(u'\\textbf{')
    context.write(title)
    context.write(u'}\\\\\n')
    render_children(context, node)
    return node


@component.adapter(ICNXProblemSolution)
@interface.implementer(IRenderer)
class CNXProblemSolutionRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        return render_cnx_problem_solution(context, node)
    __call__ = render
