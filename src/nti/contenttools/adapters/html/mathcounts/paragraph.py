#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.adapters.html.mathcounts import check_child
from nti.contenttools.adapters.html.mathcounts import check_element_text
from nti.contenttools.adapters.html.mathcounts import check_element_tail


class Paragraph(types.Paragraph):

    @classmethod
    def process(cls, element, styles=(), html=None):
        me = cls()
        attrib = element.attrib
        me.styles.extend(styles)
        me = check_element_text(me, element)
        me = check_child(me, element, html)
        me = check_element_tail(me, element)

        if 'class' in attrib:
            if 'Normal' in attrib['class']:
                html.naq_counter = html.naq_counter + 1
                label = u'%s_%s' % (html.labelling, html.naq_counter)
                label = create_label('naqsymmath', label)
                me = create_symmath_node(me, label)
        return me


def create_symmath_node(node, label=None):
    """
    This function basically creates {naqsymmathpart} env with empty solution and explanation
    """
    naqsymmath = types.NaqSymmath()
    if label:
        naqsymmath.label = label
    naqsymmathpart = types.NaqSymmathPart()
    naqsymmathpart.text = node
    naqsymmathpart.solution = types.NaqSymmathPartSolution()
    naqsymmathpart.solution.value = types.NaqSymmathPartSolutionValue()
    naqsymmathpart.explanation = types.NaqSymmathPartSolutionExplanation()
    naqsymmath.add(naqsymmathpart)
    return naqsymmath
