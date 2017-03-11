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

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_command
from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output
from nti.contenttools.renderers.LaTeX.base import render_node_with_newline

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IMtr
from nti.contenttools.types.interfaces import IMtd
from nti.contenttools.types.interfaces import IMath
from nti.contenttools.types.interfaces import IMRow
from nti.contenttools.types.interfaces import IMSub
from nti.contenttools.types.interfaces import IMSup
from nti.contenttools.types.interfaces import IMFrac
from nti.contenttools.types.interfaces import IMNone
from nti.contenttools.types.interfaces import IMOver
from nti.contenttools.types.interfaces import IMRoot
from nti.contenttools.types.interfaces import IMsqrt
from nti.contenttools.types.interfaces import IMText
from nti.contenttools.types.interfaces import IMTable
from nti.contenttools.types.interfaces import IMUnder
from nti.contenttools.types.interfaces import IMFenced
from nti.contenttools.types.interfaces import IMathRun
from nti.contenttools.types.interfaces import IMSubSup
from nti.contenttools.types.interfaces import IMMenclose
from nti.contenttools.types.interfaces import IMUnderover
from nti.contenttools.types.interfaces import IMMultiscripts
from nti.contenttools.types.interfaces import IMMprescripts


"""
rendering MathML element
"""


def render_math_html(context, node):
    """
    render element <math>
    """
    if len(node.children) == 0:
        context.write(u'')
    elif node.equation_type == u'inline':
        context.write(u'\\(')
        render_children(context, node)
        context.write(u'\\)')
    else:
        context.write(u'\\[')
        render_children(context, node)
        context.write(u'\\]')
    return node


def render_mrow(context, node):
    return render_children(context, node)


def render_mfenced(context, node):
    """
    render element <mfenced>
    """
    if node.children:
        if IMTable.providedBy(node.children[0]):
            return set_matrix_border(context, node)
        elif IMRow.providedBy(node.children[0]):
            if node.children[0].children or ():
                if IMTable.providedBy(node.children[0].children[0]):
                    return set_matrix_border(context, node)
                else:
                    return set_mfenced_without_border(context, node)
            else:
                return set_mfenced_without_border(context, node)
        else:
            return set_mfenced_without_border(context, node)
    else:
        context.write(u'')
    return node


def set_matrix_border(context, node):
    if node.opener == u'[':
        context.write(u'\\begin{bmatrix}\n')
        render_children(context, node)
        context.write(u'\\end{bmatrix}\n')
    elif node.opener == u'(':
        context.write(u'\\begin{pmatrix}\n')
        render_children(context, node)
        context.write(u'\\end{pmatrix}\n')
    else:
        context.write(u'\\begin{matrix}\n')
        render_children(context, node)
        context.write(u'\\end{matrix}\n')
    return node


def set_mfenced_without_border(context, node):
    context.write(node.opener)
    render_children(context, node)
    context.write(node.close)
    return node


def render_math_run(context, node):
    """
    render MathRun node <mi>, <mo>, <mn>
    """
    return render_children(context, node)


def render_mtable(context, node):
    """
    render <mtable> element
    """
    number_of_col = int(node.number_of_col)
    string_col = u''
    for unused in range(number_of_col):
        string_col = string_col + u' l '

    result = None
    if node.__parent__:
        if IMFenced.providedBy(node.__parent__):
            result = render_children(context, node)
        elif IMRow.providedBy(node.__parent__):
            if node.__parent__.__parent__:
                if IMFenced.providedBy(node.__parent__.__parent__):
                    result = render_children(context, node)
                else:
                    result = set_array_environment(context, node, string_col)
            else:
                result = set_array_environment(context, node, string_col)
        else:
            result = set_array_environment(context, node, string_col)
    else:
        result = set_array_environment(context, node, string_col)
    return result


def set_array_environment(context, node, string_col):
    string_col = u'\\begin{array}{%s}\n' % (string_col)
    context.write(string_col)
    render_children(context, node)
    context.write(u'\\end{array}')
    return node


def render_mtr(context, node):
    """
    render <mtr> element
    """
    context.write(render_node_with_newline(node))
    return node


def render_mtd(context, node):
    """
    to render <mtd> element
    """
    return render_children(context, node)


def render_mfrac(context, node):
    """
    render <mfrac> element
    """
    if len(node.children) != 2:
        logger.warn("<MFrac> should only have 2 children")
    else:
        context.write(u'\\frac{')
        render_node(context, node.children[0])
        context.write(u'}{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_msub(context, node):
    """
    render <msub> element
    """
    if len(node.children) != 2:
        logger.warn('<msub> element should have 2 children')
    else:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}_{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_msup(context, node):
    """
    render <msup> element
    """
    if len(node.children) != 2:
        logger.warn('<msup> element should have 2 children')
    else:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}^{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_msubsup(context, node):
    """
    render <msubsup> element
    """
    check = render_children_output(node.children[0])
    if len(node.children) != 3:
        logger.warn("<msubsup> should only have 3 children")
    elif u'int' in check:
        context.write(u'\\int_{')
    elif u'sum' in check:
        context.write(u'\\sum_{')
    elif u'prod' in check:
        context.write(u'\\prod_{')
    else:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}_{')
    render_node(context, node.children[1])
    context.write(u'}^{')
    render_node(context, node.children[2])
    context.write(u'}')
    return node


def render_msqrt(context, node):
    """
    render <msqrt> element
    """
    context.write(u'\\sqrt{')
    render_children(context, node)
    context.write(u'}')
    return node


def render_mroot(context, node):
    """
    render <mroot> element
    """
    if len(node.children) != 2:
        logger.warn("<MRoot> should only have 2 children")
    else:
        context.write(u'\\sqrt[')
        render_node(context, node.children[0])
        context.write(u']{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_munder(context, node):
    """
    render <munder> element
    """
    if len(node.children) == 2:
        base_1 = render_output(node.children[0])
        base_2 = render_output(node.children[1])
        if u'23df' in base_2.lower() or u'\u23df' in unicode(base_2).split():
            context.write(u'\\underbrace{')
            context.write(base_1)
            context.write(u'}')
        elif u'\u220f' in unicode(base_1).split() or u'\\prod' in base_1:
            context.write(u'\\prod{')
            context.write(base_2)
            context.write(u'}')
        else:
            context.write(u'\\underset{')
            context.write(base_2)
            context.write(u'}{')
            context.write(base_1)
            context.write(u'}')
    else:
        logger.warn("mathml <munder> element should have 2 children")

    return node


def render_munderover(context, node):
    """
    render <munderover> element
    """
    if len(node.children) == 3:
        token = render_output(node.children[0])
        if u'\u2211' in unicode(token.split()) or u'\\sum' in token:
            context.write(u'\\sum_{')
            render_node(context, node.children[1])
            context.write(u'}^{')
            render_node(context, node.children[2])
            context.write(u'}')
        elif u'\u222b' in unicode(token.split()) or u'\\int' in token:
            context.write(u'\\int_{')
            render_node(context, node.children[1])
            context.write(u'}^{')
            render_node(context, node.children[2])
            context.write(u'}')
        elif u'\u220f' in unicode(token.split()) or u'\\prod' in token:
            context.write(u'\\prod_{')
            render_node(context, node.children[1])
            context.write(u'}^{')
            render_node(context, node.children[2])
            context.write(u'}')
        else:
            context.write(u'\\overset{')
            render_node(context, node.children[2])
            context.write(u'}{\\underset{')
            render_node(context, node.children[1])
            context.write(u'}{')
            context.write(token)
            context.write(u'}}')
    else:
        logger.warn(u'The number <munderover> element child is not 3')
    return node


def render_mover(context, node):
    """
    render <mover> element
    """
    base = render_output(node.children[1])
    if u'23de' in base.lower() or u'\u23de' in unicode(base).split():
        context.write(u'\\overbrace{')
        render_node(context, node.children[0])
        context.write(u'}')
    else:
        context.write(u'\\overset{')
        context.write(base)
        context.write(u'}{')
        render_node(context, node.children[0])
        context.write(u'}')
    return node


def render_mmultiscript(context, node):
    """
    render <mmultiscript> element
    """
    if node.prescripts and node.base:
        render_node(context, node.prescripts)
        render_node(context, node.base)
    else:
        logger.warn(u'<mmultiscript> prescripts or base is None')
    return node


def render_mprescripts(context, node):
    """
    render <mprescripts> element
    """
    if node.sub and node.sup:
        context.write(u'{_{')
        render_node(context, node.sub)
        context.write(u'}^{')
        render_node(context, node.sup)
        context.write(u'}}')
    else:
        logger.warn('prescripts sub or sup is None')
    return node


def render_mnone(context, node):
    """
    render <none/> element
    """
    context.write(u'')
    return node


def render_mtext(context, node):
    """
    render <mtext> element
    """
    base = render_children_output(node)
    if base:
        context.write(u'\\text{')
        context.write(base)
        context.write(u'}')
    return node


def render_menclose(context, node):
    """
    render <menclose> element
    """
    notation = list(node.notation.split())
    for item in notation:
        if item == u'updiagonalstrike':
            # TODO : need to use package : cancel, uncomment if we are able to
            # use cancel
            m_updiagonalstrike(context, node)
        elif item == u'downdiagonalstrike':
            # TODO : need to use package : cancel, uncomment if we are able to
            # use cancel
            m_downdiagonalstrike(context, node)
        elif item == 'radical':
            m_radical(context, node)
        elif item == 'left':
            m_left(context, node)
        elif item == 'right':
            m_right(context, node)
        elif item == 'top':
            m_top(context, node)
        elif item == 'bottom':
            m_bottom(context, node)
        elif item == 'verticalstrike':
            # TODO : need to use package : cancel, uncomment if we are able to
            # use cancel
            pass
        elif item == 'horizontalstrike':
            # TODO : need to use package : cancel, uncomment if we are able to
            # use cancel
            m_horizontalstrike(context, node)
            pass
        elif item == 'madruwb':
            # TODO : create a method to handle this notation
            pass
        elif item == 'updiagonalarrow':
            # TODO : create a method to handle this notation
            pass
        elif item == 'phasorangle':
            # TODO : create a method to handle this notation
            pass
        elif item == 'actuarial':
            # TODO : create a method to handle this notation
            pass
        elif item == 'box':
            m_box(context, node)
        elif item == 'roundedbox':
            # TODO : create a method to handle this notation
            pass
        elif item == 'circle':
            # TODO : create a method to handle this notation
            pass
        elif item == 'longdiv':
            m_longdiv(context, node)
    return node


def m_radical(context, node):
    return render_command(context, u'sqrt', node)


def m_updiagonalstrike(context, node):
    return render_command(context, u'cancel', node)


def m_downdiagonalstrike(context, node):
    return render_command(context, u'bcancel', node)


def m_horizontalstrike(context, node):
    return render_command(context, u'hcancel', node)


def m_top(context, node):
    return render_command(context, u'overline', node)


def m_bottom(context, node):
    return render_command(context, u'underline', node)


def m_box(context, node):
    return render_command(context, u'boxed', node)


def m_longdiv(context, node):
    # TODO : the render result will look odd, find a better command
    return render_command(context, u'overline', node)


def m_left(context, node):
    context.write(u'\\Big|')
    render_children(context, node)
    return node


def m_right(context, node):
    render_children(context, node)
    context.write(u'\\Big|')
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


@component.adapter(IMath)
class MathRenderer(RendererMixin):
    func = staticmethod(render_math_html)


@component.adapter(IMRow)
class MRowRenderer(RendererMixin):
    func = staticmethod(render_mrow)


@component.adapter(IMFenced)
class MFencedRenderer(RendererMixin):
    func = staticmethod(render_mfenced)


@component.adapter(IMathRun)
class MathRunRenderer(RendererMixin):
    func = staticmethod(render_math_run)


@component.adapter(IMTable)
class MTableRenderer(RendererMixin):
    func = staticmethod(render_mtable)


@component.adapter(IMtr)
class MtrRenderer(RendererMixin):
    func = staticmethod(render_mtr)


@component.adapter(IMtd)
class MtdRenderer(RendererMixin):
    func = staticmethod(render_mtd)


@component.adapter(IMFrac)
class MFracRenderer(RendererMixin):
    func = staticmethod(render_mfrac)


@component.adapter(IMSub)
class MSubRenderer(RendererMixin):
    func = staticmethod(render_msub)


@component.adapter(IMSup)
class MSupRenderer(RendererMixin):
    func = staticmethod(render_msup)


@component.adapter(IMSubSup)
class MSubSupRenderer(RendererMixin):
    func = staticmethod(render_msubsup)


@component.adapter(IMsqrt)
class MSqrtRenderer(RendererMixin):
    func = staticmethod(render_msqrt)


@component.adapter(IMRoot)
class MRootRenderer(RendererMixin):
    func = staticmethod(render_mroot)


@component.adapter(IMUnder)
class MUnderRenderer(RendererMixin):
    func = staticmethod(render_munder)


@component.adapter(IMUnderover)
class MUnderoverRenderer(RendererMixin):
    func = staticmethod(render_munderover)


@component.adapter(IMOver)
class MOverRenderer(RendererMixin):
    func = staticmethod(render_mover)


@component.adapter(IMMultiscripts)
class MMultiscriptsRenderer(RendererMixin):
    func = staticmethod(render_mmultiscript)


@component.adapter(IMMprescripts)
class MprescriptsRenderer(RendererMixin):
    func = staticmethod(render_mprescripts)


@component.adapter(IMNone)
class MNoneRenderer(RendererMixin):
    func = staticmethod(render_mnone)


@component.adapter(IMText)
class MTextRenderer(RendererMixin):
    func = staticmethod(render_mtext)


@component.adapter(IMMenclose)
class MencloseRenderer(RendererMixin):
    func = staticmethod(render_menclose)
