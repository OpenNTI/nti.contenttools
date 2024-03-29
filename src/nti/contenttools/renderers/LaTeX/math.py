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
from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_command
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_iterable
from nti.contenttools.renderers.LaTeX.base import render_children_output
from nti.contenttools.renderers.LaTeX.base import render_node_with_newline

from nti.contenttools.renderers.LaTeX.utils import create_label

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
from nti.contenttools.types.interfaces import IMLabeledTr
from nti.contenttools.types.interfaces import IMMprescripts
from nti.contenttools.types.interfaces import IMMultiscripts


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
    node = check_mfenced_open_close(node)
    context.write(node.opener)
    check = len(node.children) - 1
    if node.separators:
        separators = list(node.separators)
        diff = check - len(separators)
        if diff > 0:
            ext_list = [separators[-1]] * diff
            separators.extend(ext_list)
        elif diff < 0:
            separators = separators[0:check]
        render_mfenced_children(context, node, separators)
    else:
        separators = [u','] * check
        render_mfenced_children(context, node, separators)
    context.write(node.close)
    return node


def check_mfenced_open_close(node):
    if not node.opener:
        node.opener = u'('
    elif node.opener == u'{':
        node.opener = u'\{'

    if not node.close:
        node.close = u')'
    elif node.close == u'}':
        node.close = u'\}'
    return node


def render_mfenced_children(context, node, separators):
    render_node(context, node.children[0])
    for i, sep in enumerate(separators):
        context.write(sep)
        render_node(context, node.children[i + 1])
    return node


INVISIBLE_OPERATORS = (u'\u2061', u'\u2062', u'\u2063', u'\u2064')


def render_math_run(context, node):
    """
    render MathRun node <mi>, <mo>, <mn>
    """
    output = render_children_output(node)
    if node.element_type == u'operator':
        if output.strip() in INVISIBLE_OPERATORS:
            context.write(u'\\,')
        elif output.strip() == u'there exists':
            context.write(u'\\exists ')
        elif output.strip() == u'such that':
            context.write(u'\\ni ')
        else:
            context.write(output)
    else:
        context.write(output)
    return node


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


def render_mlabeledtr(context, node):
    """
    render <mlabeledtr> element
    """
    if node.children:
        tag = render_output(node.children[0])
        label = create_label('mlabeledtr', tag)
        children_num = len(node.children)
        render_iterable(context, node.children[1:children_num])
        context.write(u' \\tag{')
        context.write(tag)
        context.write(u'} ')
        context.write(label)
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
        render_node(context, node.children[1])
        context.write(u']{')
        render_node(context, node.children[0])
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


check_env_char = (u'\u02C5', u'\u02C7', u'0076', u'\\textasciicaron')

ddot_env_char = (u'\u00A8', u'\\textasciidieresis', u'\u0308',
                 u'\\"', u'\u0324')

dot_env_char = (u'\u0323', u'\u00B7', u'\u002E', u'\\cdot')

grave_env_char = (u'\u0060', u'\\textasciigrave', u'\u02CB')

mathring_env_char = (u'\u00B0', u'\\textdegree', u'\u02DA',
                     u'\\r{}', u'\u02F3', u'\u0325')

tilde_env_char = (u'~', u'\u007E', u'\\textasciitilde',
                  u'\u02F7', u'\u0303')

vec_env_char = (u'\u2192', u'\\rightarrow')


def render_mover(context, node):
    """
    render <mover> element
    """
    base = render_output(node.children[1])
    if u'\u23de' in base:
        context.write(u'\\overbrace{')
        render_node(context, node.children[0])
        context.write(u'}')
    elif u'\u005E' in base or u'^' in base:
        render_command(context, u'hat', node.children[0])
    elif u'\u00B4' in base or u'\\textasciiacute' in base:
        render_command(context, u'acute', node.children[0])
    elif u'\u002A' in base or u'\\ast' in base:
        render_command(context, u'asteraccent', node.children[0])
    elif u'\u005F' in base:
        render_command(context, u'bar', node.children[0])
    elif u'\u02D8' in base or u'\\textasciibreve' in base:
        render_command(context, u'breve', node.children[0])
    elif any(c in base for c in check_env_char):
        render_command(context, u'check', node.children[0])
    elif any(c in base for c in ddot_env_char):
        render_command(context, u'ddot', node.children[0])
    elif any(c in base for c in dot_env_char):
        render_command(context, u'dot', node.children[0])
    elif any(c in base for c in grave_env_char):
        render_command(context, u'grave', node.children[0])
    elif any(c in base for c in mathring_env_char):
        render_command(context, u'mathring', node.children[0])
    elif any(c in base for c in tilde_env_char):
        render_command(context, u'tilde', node.children[0])
    elif any(c in base for c in vec_env_char):
        render_command(context, u'vec', node.children[0])
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
    if node.prescripts:
        render_node(context, node.prescripts)
    else:
        logger.warn(u'<mmultiscript> prescripts is None')

    if node.base:
        render_mmultiscripts_base(context, node)
    else:
        logger.warn(u'<mmultiscript> base is None')
    return node


def render_mmultiscripts_base(context, node):
    if len(node.base) == 3:
        render_node(context, node.base[0])
        context.write(u'_{')
        render_node(context, node.base[1])
        context.write(u'}^{')
        render_node(context, node.base[2])
        context.write(u'}')
    else:
        logger.warn('mmultiscripts base does not have 3 sub node')
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
    TODO : mtext shoud be able to handle string /* and */ correctly:
    mtext.add(TextNode(u' /* comment here */ ', type_text='math'))
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
            # TODO: need to use package : cancel, uncomment if we are able to
            # use cancel
            m_updiagonalstrike(context, node)
        elif item == u'downdiagonalstrike':
            # TODO: need to use package : cancel, uncomment if we are able to
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
            # TODO: need to use package : cancel, uncomment if we are able to
            # use cancel
            pass
        elif item == 'horizontalstrike':
            # TODO: need to use package : cancel, uncomment if we are able to
            # use cancel
            m_horizontalstrike(context, node)
            pass
        elif item == 'madruwb':
            # TODO: create a method to handle this notation
            pass
        elif item == 'updiagonalarrow':
            # TODO: create a method to handle this notation
            pass
        elif item == 'phasorangle':
            # TODO: create a method to handle this notation
            pass
        elif item == 'actuarial':
            # TODO: create a method to handle this notation
            pass
        elif item == 'box':
            m_box(context, node)
        elif item == 'roundedbox':
            # TODO: create a method to handle this notation
            pass
        elif item == 'circle':
            # TODO: create a method to handle this notation
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
    # TODO: the render result will look odd, find a better command
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


@component.adapter(IMLabeledTr)
class MLabeledTrRenderer(RendererMixin):
    func = staticmethod(render_mlabeledtr)
