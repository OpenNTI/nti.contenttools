#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx
from .. import types
from .ignored_tags import IGNORED_TAGS


class OMath(types.OMath):

    @classmethod
    def process(cls, omath, doc):
        me = cls()
        for element in omath.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <o:math> element %s', element.tag)
        return me


class OMathRun(types.OMathRun):

    @classmethod
    def process(cls, mathrun, doc, rels=None):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        doc_main_prefix = docx.nsprefixes['w']
        t_el = '{%s}t' % (doc_math_prefix)
        rpr_el_m = '{%s}rPr' % (doc_math_prefix)
        rpr_el = '{%s}rPr' % (doc_main_prefix)
        for element in mathrun.iterchildren():
            if element.tag == t_el:
                if element.text:
                    me.add_child(types.TextNode(element.text, type_text='omath'))
            elif element.tag == rpr_el:
                pass
            elif element.tag == rpr_el_m:
                pass
            elif element.tag in IGNORED_TAGS:
                pass
            else:
                logger.warn('Unhandled <m:r> element %s', element.tag)
        return me


class OMathFrac(types.OMathFrac):

    @classmethod
    def process(cls, mathfrac, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        num_el = '{%s}num' % (doc_math_prefix)
        den_el = '{%s}den' % (doc_math_prefix)
        fPr_el = '{%s}fPr' % (doc_math_prefix)
        type_el = '{%s}type' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in mathfrac.iterchildren():
            if element.tag == num_el:
                me.add_child(OMathNumerator.process(element, doc))
            elif element.tag == den_el:
                me.add_child(OMathDenominator.process(element, doc))
            elif element.tag == fPr_el:
                for el in element.iterchildren():
                    if el.tag == type_el:
                        me.set_frac_type(unicode(el.attrib[att_val]))
        return me


class OMathNumerator(types.OMathNumerator):

    @classmethod
    def process(cls, mathnum, doc):
        me = cls()
        for element in mathnum.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:num> element %s', element.tag)
        return me


class OMathDenominator(types.OMathDenominator):

    @classmethod
    def process(cls, mathden, doc):
        me = cls()
        for element in mathden.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:den> element %s', element.tag)
        return me


class OMathRadical(types.OMathRadical):

    @classmethod
    def process(cls, mathrad, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        radPr_el = '{%s}radPr' % (doc_math_prefix)
        deg_el = '{%s}deg' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        for element in mathrad.iterchildren():
            if element.tag == radPr_el:
                pass
            elif element.tag == deg_el:
                me.add_child(OMathDegree.process(element, doc))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
        return me


class OMathDegree(types.OMathDegree):

    @classmethod
    def process(cls, mathdeg, doc):
        me = cls()
        for element in mathdeg.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:deg> element %s', element.tag)
        return me


class OMathBase(types.OMathBase):

    @classmethod
    def process(cls, mathbase, doc):
        me = cls()
        for element in mathbase.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:e> element %s', element.tag)
        return me


class OMathSuperscript(types.OMathSuperscript):

    @classmethod
    def process(cls, mathsup, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        sSupPr_el = '{%s}sSupPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        sup_el = '{%s}sup' % (doc_math_prefix)
        for element in mathsup.iterchildren():
            if element.tag == sSupPr_el:
                pass
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == sup_el:
                me.add_child(OMathSup.process(element, doc))
            else:
                logger.warn('Unhandled <m:sSup> element %s', element.tag)
        return me


class OMathSup(types.OMathSup):

    @classmethod
    def process(cls, msup, doc):
        me = cls()
        for element in msup.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn("Unhandled <m:sup> %s", element.tag)
        return me


class OMathSubscript(types.OMathSubscript):

    @classmethod
    def process(cls, mathsub, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        sSubPr_el = '{%s}sSubPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        sub_el = '{%s}sub' % (doc_math_prefix)
        for element in mathsub.iterchildren():
            if element.tag == sSubPr_el:
                pass
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == sub_el:
                me.add_child(OMathSub.process(element, doc))
            else:
                logger.warn('Unhandled <m:sSup> element %s', element.tag)
        return me


class OMathSub(types.OMathSub):

    @classmethod
    def process(cls, msub, doc):
        me = cls()
        for element in msub.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn("Unhandled <m:sub> %s", element.tag)
        return me


class OMathSubSup(types.OMathSubSup):

    @classmethod
    def process(cls, msubsup, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        sSubSupPr_el = '{%s}sSubSupPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        sub_el = '{%s}sub' % (doc_math_prefix)
        sup_el = '{%s}sup' % (doc_math_prefix)
        for element in msubsup.iterchildren():
            if element.tag == sSubSupPr_el:
                pass
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == sub_el:
                me.add_child(OMathSub.process(element, doc))
            elif element.tag == sup_el:
                me.add_child(OMathSup.process(element, doc))
            else:
                logger.warn('Unhandled <m:sSubSup> element %s', element.tag)
        return me


class OMathNary(types.OMathNary):

    @classmethod
    def process(cls, mnary, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        naryPr_el = '{%s}naryPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        sub_el = '{%s}sub' % (doc_math_prefix)
        sup_el = '{%s}sup' % (doc_math_prefix)
        for element in mnary.iterchildren():
            if element.tag == naryPr_el:
                me.add_child(OMathNaryPr.process(element, doc))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == sub_el:
                me.add_child(OMathSub.process(element, doc))
            elif element.tag == sup_el:
                me.add_child(OMathSup.process(element, doc))
            else:
                logger.warn('Unhandled <m:naryPr> element %s', element.tag)
        return me


class OMathNaryPr(types.OMathNaryPr):

    @classmethod
    def process(cls, mnarypr, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        chr_el = '{%s}chr' % (doc_math_prefix)
        limLoc_el = '{%s}limLoc' % (doc_math_prefix)
        grow_el = '{%s}grow' % (doc_math_prefix)
        subHide_el = '{%s}subHide' % (doc_math_prefix)
        supHide_el = '{%s}supHide' % (doc_math_prefix)
        ctrlPr_el = '{%s}ctrlPr' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in mnarypr.iterchildren():
            if element.tag == chr_el:
                me.add_child(process_omath_chr_attributes(element, doc))
                me.set_chr_val(element.attrib[att_val])
            elif element.tag == limLoc_el:
                me.set_lim_loc_val(unicode(element.attrib[att_val]))
            elif element.tag == grow_el:
                pass
            elif element.tag == subHide_el:
                pass
            elif element.tag == supHide_el:
                pass
            elif element.tag == ctrlPr_el:
                pass
            else:
                logger.warn('Unhandled <m:naryPr> element %s', element.tag)
        return me


def process_omath_chr_attributes(element, doc):
    chr_val = element.attrib['{' + docx.nsprefixes['m'] + '}val']
    el = types.TextNode(chr_val, type_text='omath')
    return el


class OMathDelimiter(types.OMathDelimiter):

    @classmethod
    def process(cls, md, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        dPr_el = '{%s}dPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        for element in md.iterchildren():
            if element.tag == dPr_el:
                me.add_child(OMathDPr.process(element, doc))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:d> element %s', element.tag)
        return me


class OMathDPr(types.OMathDPr):

    @classmethod
    def process(cls, mdpr, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        begChr_el = '{%s}begChr' % (doc_math_prefix)
        endChr_el = '{%s}endChr' % (doc_math_prefix)
        ctrlPr_el = '{%s}ctrlPr' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in mdpr.iterchildren():
            if element.tag == begChr_el:
                begChr = unicode(element.attrib[att_val])
                me.set_beg_char(begChr)
                me.add_child(types.TextNode(begChr, type_text='omath'))
            elif element.tag == endChr_el:
                endChr = element.attrib[att_val]
                me.set_end_char(endChr)
                me.add_child(types.TextNode(endChr, type_text='omath'))
            elif element.tag == ctrlPr_el:
                pass
            else:
                logger.warn('Unhandled <m:dPr> element %s', element.tag)
        return me


class OMathLimLow(types.OMathLimLow):

    @classmethod
    def process(cls, mlimlow, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        lim_el = '{%s}lim' % (doc_math_prefix)
        limLowPr_el = '{%s}limLowPr' % (doc_math_prefix)
        for element in mlimlow.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == lim_el:
                me.add_child(OMathLim.process(element, doc))
            elif element.tag == limLowPr_el:
                pass
            else:
                logger.warn('Unhandled <m:limlow> element %s', element.tag)
        return me


class OMathLim(types.OMathLim):

    @classmethod
    def process(cls, mlim, doc):
        me = cls()
        for element in mlim.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:lim> element %s', element.tag)
        return me


class OMathBar(types.OMathBar):

    @classmethod
    def process(cls, mbar, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        barPr_el = '{%s}barPr' % (doc_math_prefix)
        pos_el = '{%s}pos' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in mbar.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == barPr_el:
                for el in element.iterchildren():
                    if el.tag == pos_el:
                        me.set_bar_pos(el.attrib[att_val])
            else:
                logger.warn('Unhandled <m:bar> element %s', element.tag)
        return me


class OMathAcc(types.OMathAcc):

    @classmethod
    def process(cls, macc, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        accPr_el = '{%s}accPr' % (doc_math_prefix)
        chr_el = '{%s}chr' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in macc.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == accPr_el:
                for el in element.iterchildren():
                    if el.tag == chr_el:
                        me.set_acc_chr(el.attrib[att_val])
            else:
                logger.warn('Unhandled <m:bar> element %s', element.tag)
        return me


class OMathPara(types.OMathPara):

    @classmethod
    def process(cls, mpara, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        oMathParaPr_el = '{%s}oMathParaPr' % (doc_math_prefix)
        oMath_el = '{%s}oMath' % (doc_math_prefix)
        for element in mpara.iterchildren():
            if element.tag == oMathParaPr_el:
                pass
            elif element.tag == oMath_el:
                me.add_child(OMath.process(element, doc))
            else:
                logger.warn('Unhandled <m:oMathPara> element %s', element.tag)
        return me


class OMathMatrix(types.OMathMatrix):

    @classmethod
    def process(cls, mm, doc):
        me = cls()
        number_of_row = 0
        number_of_col = 0
        doc_math_prefix = docx.nsprefixes['m']
        mPr_el = '{%s}mPr' % (doc_math_prefix)
        mr_el = '{%s}mr' % (doc_math_prefix)
        for element in mm.iterchildren():
            if element.tag == mPr_el:
                number_of_col = process_matrix_property(element, doc)
                me.set_number_of_col(number_of_col)
            elif element.tag == mr_el:
                number_of_row = number_of_row + 1
                me.add_child(OMathMr.process(element, doc))
            else:
                logger.warn('Unhandled <m:m> element %s', element.tag)
        me.set_number_of_row(number_of_row)
        return me


def process_matrix_property(element, doc):
    number_of_col = 0
    doc_math_prefix = docx.nsprefixes['m']
    ctrlPr_el = '{%s}ctrlPr' % (doc_math_prefix)
    mcs_el = '{%s}mcs' % (doc_math_prefix)
    mc_el = '{%s}mc' % (doc_math_prefix)
    for sub_element in element.iterchildren():
        if sub_element.tag == ctrlPr_el:
            pass
        elif sub_element.tag == mcs_el:
            for el in sub_element.iterchildren():
                if el.tag == mc_el:
                    number_of_col = process_mc(el, doc)
        else:
            logger.warn('Unhandled <mPr> element %s', sub_element.tag)
    return number_of_col


def process_mc(element, doc):
    number_of_col = 0
    doc_math_prefix = docx.nsprefixes['m']
    mcPr_el = '{%s}mcPr' % (doc_math_prefix)
    count_el = '{%s}count' % (doc_math_prefix)
    att_val = '{%s}val' % (doc_math_prefix)
    for sub_element in element.iterchildren():
        if sub_element.tag == mcPr_el:
            for el in sub_element.iterchildren():
                if el.tag == count_el:
                    number_of_col = el.attrib[att_val]
        else:
            logger.warn('Unhandled <m:mcs> element %s', sub_element.tag)
    return number_of_col


class OMathMr(types.OMathMr):

    @classmethod
    def process(cls, mr, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        for element in mr.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:e> element %s', element.tag)
        return me


class OMathFunc(types.OMathFunc):

    @classmethod
    def process(cls, mfunc, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        funcPr_el = '{%s}funcPr' % (doc_math_prefix)
        fName_el = '{%s}fName' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        for element in mfunc.iterchildren():
            if element.tag == funcPr_el:
                pass
            elif element.tag == fName_el:
                me.add_child(OMathFName.process(element, doc))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:func> element %s', element.tag)
        return me


class OMathFName(types.OMathFName):

    @classmethod
    def process(cls, mfname, doc):
        me = cls()
        for element in mfname.iterchildren():
            new_child = OMathElement.create_child(element, doc)
            if new_child is not None:
                me.add_child(new_child)
            else:
                logger.warn('Unhandled <m:fName> element %s', element.tag)
        return me


class OMathEqArr(types.OMathEqArr):

    @classmethod
    def process(cls, meqarr, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        eqArrPr_el = '{%s}eqArrPr' % (doc_math_prefix)
        rSp_el = '{%s}rSp' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        att_val = '{%s}val' % (doc_math_prefix)
        for element in meqarr.iterchildren():
            if element.tag == eqArrPr_el:
                for el in element.iterchildren():
                    if el.tag == rSp_el:
                        row_space = el.attrib[att_val]
                        me.set_row_space(row_space)
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:eqArr> element %s', element.tag)
        return me


class OMathSPre(types.OMathSPre):

    @classmethod
    def process(cls, mspre, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        sPrePr_el = '{%s}sPrePr' % (doc_math_prefix)
        sub_el = '{%s}sub' % (doc_math_prefix)
        sup_el = '{%s}sup' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        for element in mspre.iterchildren():
            if element.tag == sPrePr_el:
                pass
            elif element.tag == sub_el:
                me.add_child(OMathSub.process(element, doc))
            elif element.tag == sup_el:
                me.add_child(OMathSup.process(element, doc))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:sPre> element %s', element.tag)
        return me


class OMathBox(types.OMathBox):

    @classmethod
    def process(cls, mbox, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        boxPr_el = '{%s}boxPr' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        for element in mbox.iterchildren():
            if element.tag == boxPr_el:
                pass
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:box> element %s', element.tag)
        return me


class OMathGroupChr(types.OMathGroupChr):

    @classmethod
    def process(cls, mbox, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        groupChrPr_el = '{%s}groupChrPr' % (doc_math_prefix)
        chr_el = '{%s}chr' % (doc_math_prefix)
        vertJc_el = '{%s}vertJc' % (doc_math_prefix)
        pos_el = '{%s}pos' % (doc_math_prefix)
        e_el = '{%s}e' % (doc_math_prefix)
        val_att = '{%s}val' % (doc_math_prefix)
        for element in mbox.iterchildren():
            if element.tag == groupChrPr_el:
                for el in element.iterchildren():
                    if el.tag == chr_el:
                        me.set_groupChr(el.attrib[val_att])
                    if el.tag == vertJc_el:
                        me.set_vertJc(el.attrib[val_att])
                    if el.tag == pos_el:
                        me.set_pos(unicode(el.attrib[val_att]))
            elif element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            else:
                logger.warn('Unhandled <m:groupChr> element %s', element.tag)
        return me


class OMathLimUpp(types.OMathLimUpp):

    @classmethod
    def process(cls, mlimupp, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        lim_el = '{%s}lim' % (doc_math_prefix)
        limUppPr_el = '{%s}limUppPr' % (doc_math_prefix)
        for element in mlimupp.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == lim_el:
                me.add_child(OMathLim.process(element, doc))
            elif element.tag == limUppPr_el:
                pass
            else:
                logger.warn('Unhandled <m:limUpp> element %s', element.tag)
        return me


class OMathBorderBox(types.OMathBorderBox):

    @classmethod
    def process(cls, mbdrbox, doc):
        me = cls()
        doc_math_prefix = docx.nsprefixes['m']
        e_el = '{%s}e' % (doc_math_prefix)
        borderBoxPr_el = '{%s}borderBoxPr' % (doc_math_prefix)
        for element in mbdrbox.iterchildren():
            if element.tag == e_el:
                me.add_child(OMathBase.process(element, doc))
            elif element.tag == borderBoxPr_el:
                pass
            else:
                logger.warn('Unhandled <m:borderBox> element %s', element.tag)
        return me


class OMathElement(object):

    @classmethod
    def create_child(cls, element, doc):
        doc_math_prefix = docx.nsprefixes['m']
        if element.tag == '{%s}r' % (doc_math_prefix):
            return(OMathRun.process(element, doc))
        elif element.tag == '{%s}f' % (doc_math_prefix):
            return(OMathFrac.process(element, doc))
        elif element.tag == '{%s}rad' % (doc_math_prefix):
            return(OMathRadical.process(element, doc))
        elif element.tag == '{%s}sSup' % (doc_math_prefix):
            return(OMathSuperscript.process(element, doc))
        elif element.tag == '{%s}sSub' % (doc_math_prefix):
            return(OMathSubscript.process(element, doc))
        elif element.tag == '{%s}sSubSup' % (doc_math_prefix):
            return(OMathSubSup.process(element, doc))
        elif element.tag == '{%s}nary' % (doc_math_prefix):
            return(OMathNary.process(element, doc))
        elif element.tag == '{%s}d' % (doc_math_prefix):
            return(OMathDelimiter.process(element, doc))
        elif element.tag == '{%s}limLow' % (doc_math_prefix):
            return(OMathLimLow.process(element, doc))
        elif element.tag == '{%s}t' % (doc_math_prefix):
            if element.text:
                return types.TextNode(element.text, type_text='omath')
        elif element.tag == '{%s}ctrlPr' % (doc_math_prefix):
            pass
        elif element.tag == '{%s}bar' % (doc_math_prefix):
            return(OMathBar.process(element, doc))
        elif element.tag == '{%s}acc' % (doc_math_prefix):
            return(OMathAcc.process(element, doc))
        elif element.tag == '{%s}m' % (doc_math_prefix):
            return(OMathMatrix.process(element, doc))
        elif element.tag == '{%s}func' % (doc_math_prefix):
            return(OMathFunc.process(element, doc))
        elif element.tag == '{%s}eqArr' % (doc_math_prefix):
            return(OMathEqArr.process(element, doc))
        elif element.tag == '{%s}sPre' % (doc_math_prefix):
            return(OMathSPre.process(element, doc))
        elif element.tag == '{%s}box' % (doc_math_prefix):
            return(OMathBox.process(element, doc))
        elif element.tag == '{%s}groupChr' % (doc_math_prefix):
            return(OMathGroupChr.process(element, doc))
        elif element.tag == '{%s}argPr' % (doc_math_prefix):
            logger.info('found %s', element.tag)
        elif element.tag == '{%s}limUpp' % (doc_math_prefix):
            return(OMathLimUpp.process(element, doc))
        elif element.tag == '{%s}borderBox' % (doc_math_prefix):
            return(OMathBorderBox.process(element, doc))
        else:
            logger.warn('Unhandled omath element %s', element.tag)
            return None
