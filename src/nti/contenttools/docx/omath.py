#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

#from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)

from . import properties as docx
from .. import types
from .ignored_tags import IGNORED_TAGS

class OMath(types.OMath):
	@classmethod
	def process(cls, omath, doc):
		me = cls()
		for element in omath.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <o:math> element %s',element.tag)
		return me

class OMathRun(types.OMathRun):
	@classmethod
	def process(cls, mathrun, doc, rels=None):
		me = cls()
		for element in mathrun.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}t':
				if element.text:
					me.add_child(types.TextNode(element.text, type_text = 'omath'))
			elif element.tag == '{'+docx.nsprefixes['w']+'}rPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}rPr':
				pass
			elif element.tag in IGNORED_TAGS:
				pass
			else:
				logger.warn ('Unhandled <m:r> element %s', element.tag)
		return me

class OMathFrac(types.OMathFrac):
	@classmethod
	def process(cls, mathfrac, doc):
		me = cls()
		for element in mathfrac.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}num':
				me.add_child(OMathNumerator.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}den':
				me.add_child(OMathDenominator.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}fPr':
				for el in element.iterchildren():
					if el.tag == '{'+docx.nsprefixes['m']+'}type':
						me.set_frac_type(el.attrib['{'+docx.nsprefixes['m']+'}val'])
		return me

class OMathNumerator(types.OMathNumerator):
	@classmethod
	def process(cls, mathnum, doc):
		me = cls()
		for element in mathnum.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:num> element %s',element.tag)
		return me


class OMathDenominator(types.OMathDenominator):
	@classmethod
	def process(cls, mathden, doc):
		me = cls()
		for element in mathden.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:den> element %s', element.tag)
		return me

class OMathRadical(types.OMathRadical):
	@classmethod
	def process(cls, mathrad, doc):
		me = cls()
		for element in mathrad.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}radPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}deg':
				me.add_child(OMathDegree.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element,doc))
		return me

class OMathDegree(types.OMathDegree):
	@classmethod
	def process(cls, mathdeg, doc):
		me = cls()
		for element in mathdeg.iterchildren():
			new_child = OMathElement.create_child(element,doc)
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
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:e> element %s', element.tag)
		return me

class OMathSuperscript(types.OMathSuperscript):
	@classmethod
	def process(cls, mathsup, doc):
		me = cls()
		for element in mathsup.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSupPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSup.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSup> element %s', element.tag)
		return me

class OMathSup(types.OMathSup):
	@classmethod
	def process(cls, msup, doc):
		me = cls()
		for element in msup.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn("Unhandled <m:sup> %s", element.tag)
		return me

class OMathSubscript(types.OMathSubscript):
	@classmethod
	def process(cls, mathsub, doc):
		me = cls()
		for element in mathsub.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSubPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSup> element %s', element.tag)
		return me

class OMathSub(types.OMathSub):
	@classmethod
	def process(cls, msub, doc):
		me = cls()
		for element in msub.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn("Unhandled <m:sup> %s", element.tag)
		return me


class OMathSubSup(types.OMathSubSup):
	@classmethod
	def process(cls, msubsup, doc):
		me = cls()
		for element in msubsup.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSubSupPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSubSup> element %s', element.tag)
		return me

class OMathNary(types.OMathNary):
	@classmethod
	def process(cls, mnary, doc):
		me = cls()
		for element in mnary.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}naryPr':
				me.add_child(OMathNaryPr.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:naryPr> element %s', element, tag)
		return me

class OMathNaryPr(types.OMathNaryPr):
	@classmethod
	def process(cls,mnarypr, doc):
		me = cls()
		for element in mnarypr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}chr':
				me.add_child(process_omath_chr_attributes(element, doc))
				me.set_chr_val(element.attrib['{'+docx.nsprefixes['m']+'}val'])
			elif element.tag == '{'+docx.nsprefixes['m']+'}limLoc':
				me.set_lim_loc_val(element.attrib['{'+docx.nsprefixes['m']+'}val'])
			elif element.tag == '{'+docx.nsprefixes['m']+'}grow':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}subHide':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}supHide':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
				pass
			else:
				logger.warn('Unhandled <m:naryPr> element %s',element.tag)
		return me

def process_omath_chr_attributes(element, doc):
	chr_val = element.attrib['{'+docx.nsprefixes['m']+'}val']
	el = types.TextNode(chr_val, type_text = 'omath')
	return el

class OMathDelimiter(types.OMathDelimiter):
	@classmethod
	def process(cls, md, doc):
		me = cls()
		for element in md.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}dPr':
				me.add_child(OMathDPr.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:d> element %s',element.tag)
		return me

class OMathDPr(types.OMathDPr):
	@classmethod
	def process(cls, mdpr, doc):
		me = cls()
		for element in mdpr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}begChr':
				begChr = element.attrib['{'+docx.nsprefixes['m']+'}val']
				me.set_beg_char(begChr)
				me.add_child(types.TextNode(begChr, type_text = 'omath'))
			elif element.tag == '{'+docx.nsprefixes['m']+'}endChr':
				endChr = element.attrib['{'+docx.nsprefixes['m']+'}val']
				me.set_end_char(endChr)
				me.add_child(types.TextNode(endChr, type_text = 'omath'))
			elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
				pass
			else:
				logger.warn('Unhandled <m:dPr> element %s', element.tag)
		return me

class OMathLimLow(types.OMathLimLow):
	@classmethod
	def process(cls, mlimlow, doc):
		me =cls()
		for element in mlimlow.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}lim':
				me.add_child(OMathLim.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}limLowPr':
				pass
			else:
				logger.warn('Unhandled <m:limlow> element %s', element.tag)
		return me

class OMathLim(types.OMathLim):
	@classmethod
	def process(cls, mlim, doc):
		me = cls()
		for element in mlim.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:lim> element %s', element.tag)
		return me

class OMathBar(types.OMathBar):
	@classmethod
	def process(cls, mbar, doc):
		me = cls()
		for element in mbar.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}barPr':
				pass
			else:
				logger.warn('Unhandled <m:bar> element %s', element.tag)
		return me

class OMathAcc(types.OMathAcc):
	@classmethod
	def process(cls, macc, doc):
		me = cls()
		for element in macc.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}accPr':
				pass
			else:
				logger.warn('Unhandled <m:bar> element %s', element.tag)
		return me

class OMathPara(types.OMathPara):
	@classmethod
	def process(cls, mpara, doc):
		me = cls()
		for element in mpara.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}oMathParaPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}oMath':
				me.add_child(OMath.process(element,doc))
			else:
				logger.warn('Unhandled <m:oMathPara> element %s', element.tag)
		return me

class OMathMatrix(types.OMathMatrix):
	@classmethod
	def process(cls, mm, doc):
		me = cls()
		number_of_row = 0
		number_of_col = 0
		for element in mm.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}mPr':
				number_of_col = process_matrix_property(element,doc)
				me.set_number_of_col(number_of_col)
			elif element.tag == '{'+docx.nsprefixes['m']+'}mr':
				number_of_row = number_of_row + 1
				me.add_child(OMathMr.process(element,doc))
			else:
				logger.warn('Unhandled <m:m> element %s', element.tag)
		me.set_number_of_row(number_of_row)
		return me

def process_matrix_property(element, doc):
	number_of_col = 0
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
			pass
		elif sub_element.tag == '{'+docx.nsprefixes['m']+'}mcs':
			for el in sub_element.iterchildren():
				if el.tag == '{'+docx.nsprefixes['m']+'}mc':
					number_of_col = process_mc(el, doc)
		else:
			logger.warn('Unhandled <mPr> element %s', sub_element.tag)
	return number_of_col

def process_mc(element, doc):
	number_of_col = 0
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['m']+'}mcPr':
			for el in sub_element.iterchildren():
				if el.tag == '{'+docx.nsprefixes['m']+'}count':
					number_of_col = el.attrib['{'+docx.nsprefixes['m']+'}val']
		else:
			logger.warn('Unhandled <m:mcs> element %s', sub_element.tag)
	return number_of_col


class OMathMr(types.OMathMr):
	@classmethod
	def process(cls, mr, doc):
		me = cls()
		for element in mr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:e> element %s', element.tag)
		return me

class OMathFunc(types.OMathFunc):
	@classmethod
	def process(cls, mfunc, doc):
		me =cls()
		for element in mfunc.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}funcPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}fName':
				me.add_child(OMathFName.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:func> element %s', element.tag)
		return me

class OMathFName(types.OMathFName):
	@classmethod
	def process(cls, mfname, doc):
		me =cls()
		for element in mfname.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:fName> element %s', element.tag)
		return me

class OMathEqArr(types.OMathEqArr):
	@classmethod
	def process(cls, meqarr, doc):
		me = cls()
		for element in meqarr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}eqArrPr':
				for el in  element.iterchildren():
					if el.tag == '{'+docx.nsprefixes['m']+'}rSp':
						row_space = el.attrib['{'+docx.nsprefixes['m']+'}val']
						me.set_row_space(row_space)
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:eqArr> element %s', element.tag)
		return me

class OMathSPre(types.OMathSPre):
	@classmethod
	def process(cls, mspre, doc):
		me = cls()
		for element in mspre.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sPrePr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSup.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:sPre> element %s', element.tag)
		return me

class OMathElement(object):
	@classmethod
	def create_child(cls,element,doc):
		if element.tag == '{'+docx.nsprefixes['m']+'}r':
			return(OMathRun.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}f':
			return(OMathFrac.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}rad':
			return(OMathRadical.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSup':
			return(OMathSuperscript.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSub':
			return(OMathSubscript.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSubSup':
			return(OMathSubSup.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}nary':
			return(OMathNary.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}d':
			return(OMathDelimiter.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}limLow':
			return(OMathLimLow.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}t':
			if element.text:
				return types.TextNode(element.text, type_text='omath')
		elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
			pass	
		elif element.tag == '{'+docx.nsprefixes['m']+'}bar':
			return(OMathBar.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}acc':
			return(OMathAcc.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}m':
			return(OMathMatrix.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}func':
			return(OMathFunc.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}eqArr':
			return(OMathEqArr.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sPre':
			return(OMathSPre.process(element,doc))
		else:
			logger.warn('Unhandled omath element %s', element.tag)
			return None