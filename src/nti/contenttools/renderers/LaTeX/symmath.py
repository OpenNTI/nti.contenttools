#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: symmath.py 107525 2017-02-27 09:43:34Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IDocumentStructureNode

from nti.contenttools.types.interfaces import INaqSymmath
from nti.contenttools.types.interfaces import INaqSymmathPart
from nti.contenttools.types.interfaces import INaqSymmathPartSolution
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionValue
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionExplanation

def render_naqsymmath(context, node):
	context.write("\\begin{naquestion}[individual=true]\n")
	if node.label:
		render_node(context, node.label)
	render_children(context, node)
	context.write("\n\\end{naquestion}\n")
	return node

def render_naqsymmathpart(context, node):
	context.write("\\begin{naqsymmathpart}\n")
	if node.text:
		if IDocumentStructureNode.providedBy(node.text):
			render_node(context, node.text)
		else:
			context.write(node.text)
		context.write('\n')
	if node.solution:
		if IDocumentStructureNode.providedBy(node.solution):
			render_node(context, node.solution)
		else:
			context.write(node.solution)
		context.write('\n')
	if node.explanation:
		if IDocumentStructureNode.providedBy(node.explanation):
			render_node(context, node.explanation)
		else:
			context.write(node.explanation)
		context.write('\n')
	context.write("\n\\end{naqsymmathpart}\n")
	return node

def render_naqsymmathpartsolution(context, node):
	context.write("\\begin{naqsolutions}\n")
	render_children(context, node)
	context.write("\n\\end{naqsolutions}\n")
	return node

def render_naqsymmathpartsolutionvalue(context, node):
	context.write("\\naqsolution[1] ")
	if node.value:
		if IDocumentStructureNode.providedBy(node.value):
			render_node(context, node.value)
		else:
			context.write(node.value)
		context.write('\n')
	return node

def render_naqsymmathpartsolutionexplanation(context, node):
	context.write("\\begin{naqsolexplanation}\n")
	render_children(context, node)
	context.write("\n\\end{naqsolexplanation}\n")
	return node

@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(INaqSymmath)
class NaqSymmathRenderer(RendererMixin):
    func = staticmethod(render_naqsymmath)

@component.adapter(INaqSymmathPart)
class NaqSymmathPartRenderer(RendererMixin):
    func = staticmethod(render_naqsymmathpart)

@component.adapter(INaqSymmathPartSolution)
class NaqSymmathPartSolutionRenderer(RendererMixin):
    func = staticmethod(render_naqsymmathpartsolution)

@component.adapter(INaqSymmathPartSolutionValue)
class NaqSymmathPartSolutionValueRenderer(RendererMixin):
    func = staticmethod(render_naqsymmathpartsolutionvalue)

@component.adapter(INaqSymmathPartSolutionExplanation)
class NaqSymmathPartSolutionExplanationRenderer(RendererMixin):
    func = staticmethod(render_naqsymmathpartsolutionexplanation)
