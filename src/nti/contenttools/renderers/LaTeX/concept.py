#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.types.interfaces import IConceptHierarchy
from nti.contenttools.types.interfaces import IConcept

from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_environment

from nti.contenttools.renderers.LaTeX.utils import create_label
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.renderers.interfaces import IRenderer


def render_concept_hierarchy(context, node):
    return render_environment(context, u'concepthierarchy', node)


def render_concept(context, node):
    name = get_variant_field_string_value(node.name)
    context.write(u'\\begin{concept}<')
    context.write(name)
    context.write(u'>\n')
    if not node.label:
        label = create_label('concept', name)
    else:
        label = get_variant_field_string_value(node.name)
    context.write(label)
    render_children(context, node)
    context.write(u'\n\\end{concept}\n')
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


@component.adapter(IConceptHierarchy)
class ConceptHierarchyRenderer(RendererMixin):
    func = staticmethod(render_concept_hierarchy)


@component.adapter(IConcept)
class ConceptRenderer(RendererMixin):
    func = staticmethod(render_concept)
