#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
from urlparse import urlparse
from cStringIO import StringIO

from PIL import Image as PILImage

from lxml.html import HtmlComment

from ... import types

class Chapter( types.Chapter ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child( Run.process(element, epub) )
		return me

class Section( types.Section ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child( Run.process(element, epub) )
		return me

class SubSection( types.SubSection ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child( Run.process(element, epub) )
		return me

class SubSubSection( types.SubSubSection ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child( Run.process(element, epub) )
		return me

class Paragraph( types.Paragraph ):

	@classmethod
	def process(cls, element, epub, styles=()):
		me = cls()
		me.styles.extend(styles)
		if 'id' in element.attrib.keys():
			me.add_child( Label.process( element, epub ) )

		if element.text:
			if element.text.isspace():
				pass 
			else: 
				new_el_text = element.text.rstrip() + u' '
				me.add_child( types.TextNode(new_el_text))

		for child in element:
			if child.tag == 'a':
				me.add_child( _process_a_elements( child, epub ) )
			elif child.tag == 'b':
				me.add_child( _process_b_elements( child, epub ) )
			elif child.tag == 'i':
				me.add_child( _process_i_elements( child, epub ) )
			elif child.tag == 'img':
				me.add_child( Image.process( child, epub ) )
			elif child.tag == 'p':
				me.add_child( _process_p_elements( child, epub ) )
			elif child.tag == 'span':
				me.add_child( _process_span_elements( child, epub ) )
			elif child.tag == 'sub':
				me.add_child( _process_sub_elements( child, epub ) )
			elif child.tag == 'video':
				me.add_child( Video.process( child, epub ) )
			elif child.tag == 'br':
				me.add_child( types.Newline())
				if child.tail:
					me.add_child(types.TextNode(child.tail))
			elif child.tag == 'hr':
				me.add_child(_process_hr_elements(child, epub))
			elif child.tag == 'h1':
				me.add_child(_process_h1_elements(child, epub))
			elif child.tag == 'h2':
				me.add_child(_process_h2_elements(child, epub))
			elif child.tag == 'h3':
				me.add_child(_process_h3_elements(child, epub))
			elif child.tag == 'h4':
				me.add_child(_process_h4_elements(child, epub))
			elif child.tag == 'h5':
				me.add_child(_process_h5_elements(child, epub))
			elif child.tag == 'h6':
				me.add_child(_process_h6_elements(child, epub))
			elif child.tag == 'h7':
				me.add_child(_process_h7_elements(child, epub))
			elif child.tag == 'div':
				me.add_child(_process_div_elements(child, epub))
			elif child.tag == 'blockquote':
				me.add_child(BlockQuote.process(child, epub))
			elif child.tag == 'ol':
				me.add_child(_process_ol_elements(child, epub))
			elif child.tag == 'ul':
				me.add_child(_process_ul_elements(child, epub))
			elif child.tag == 'em':
				me.add_child(_process_em_elements(child,epub))
			elif child.tag == 'section':
				me.add_child(_process_section_elements(child, epub))
			elif child.tag == 'q':
				me.add_child(_process_q_elements(child, epub))
			elif child.tag == 'strong':
				me.add_child(_process_strong_elements(child, epub))
			elif child.tag == 'sup':
				me.add_child(_process_sup_elements(child, epub))
			elif child.tag == 'big':
				me.add_child(_process_big_elements(child, epub))
			elif child.tag == 'math':
				me.add_child(_process_math_elements(child, epub))
			elif child.tag == 'code':
				me.add_child(CodeLine.process(child, epub))
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled Paragraph child: %s.',child.tag)

		if element.tail:
			me.add_child( types.TextNode( element.tail.replace('\r', '' ) ) )

		return me

class Run( types.Run ):

	@classmethod
	def process(cls, element, epub, styles=[]):
		me = cls()
		me.styles.extend(styles)
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child( types.TextNode(new_el_text))

		for child in element:
			if child.tag == 'a':
				me.add_child( _process_a_elements( child, epub ) )
			elif child.tag == 'b':
				me.add_child( _process_b_elements( child, epub ) )
			elif child.tag == 'br':
				me.add_child( types.Newline() )
				if child.tail:
					me.add_child(types.TextNode(child.tail))	
			elif child.tag == 'i':
				me.add_child( _process_i_elements( child, epub ) )
			elif child.tag == 'span':
				me.add_child( _process_span_elements( child, epub ) )
			elif child.tag == 'sub':
				me.add_child( _process_sub_elements( child, epub ) )
			elif child.tag == 'sup':
				me.add_child( _process_sup_elements( child, epub ) )
			elif child.tag == 'em':
				me.add_child( _process_em_elements( child, epub ) )
			elif child.tag == 'img':
				me.add_child(Image.process(child, epub))
			elif child.tag == 'h1':
				me.add_child(_process_h1_elements(child, epub))
			elif child.tag == 'h2':
				me.add_child(_process_h2_elements(child, epub))
			elif child.tag == 'h3':
				me.add_child(_process_h3_elements(child, epub))
			elif child.tag == 'h4':
				me.add_child(_process_h4_elements(child, epub))
			elif child.tag == 'h5':
				me.add_child(_process_h5_elements(child, epub))
			elif child.tag == 'h6':
				me.add_child(_process_h6_elements(child, epub))
			elif child.tag == 'h7':
				me.add_child(_process_h7_elements(child, epub))
			elif child.tag == 'ol':
				me.add_child(_process_ol_elements(child, epub))
			elif child.tag == 'p':
				me.add_child(_process_p_elements(child, epub))
			elif child.tag == 'div':
				me.add_child(_process_div_elements(child, epub))
			elif child.tag == 'blockquote':
				me.add_child(BlockQuote.process(child, epub))
			elif child.tag == 'ul':
				me.add_child(_process_ul_elements(child, epub))
			elif child.tag == 'hr':
				me.add_child(_process_hr_elements(child, epub))
			elif child.tag == 'big':
				me.add_child(_process_big_elements(child, epub))
			elif child.tag == 'table':
				me.add_child(_process_table_elements(child, epub))
			elif child.tag == 'strong':
				me.add_child(_process_strong_elements(child, epub))
			elif child.tag == 'math':
				me.add_child(_process_math_elements(child, epub))
			elif child.tag == 'dl':
				me.add_child(_process_dl_elements(child, epub))
			elif child.tag == 'code':
				me.add_child(_process_code_elements(child, epub))
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled Run child: %s.',child)
		if element.tail:
			_t = cls()
			_t.add_child( me )
			_t.add_child( types.TextNode( element.tail.replace('\r', '' ) ) )
			me = _t

		return me

class Hyperlink( types.Hyperlink ):

	def __init__(self):
		self.type = 'Normal'

	@classmethod
	def process(cls, link, epub ):
		me = cls()

		me.target = link.attrib['href']

		if link.text:
			me.add_child( types.TextNode( link.text ) )

		for child in link:
			me.add_child( Run.process( child, epub ) )

		return me

class Label( types.Label ):

	@classmethod
	def process(cls, label, epub ):
		me = cls()
		me.name = label.attrib['id']
		return me

class Sidebar( types.Sidebar ):

	@classmethod
	def process(cls, element, epub):
		me = cls()

		for child in element:
			if child.tag == 'div':
				el = _process_div_elements( child, epub )
				if 'class' in child.attrib.keys() and 'title' in child.attrib['class']:
					me.title = el
				else:
					me.add_child( el )
			elif child.tag == 'p':
				me.add_child( _process_p_elements( child, epub ) )
			elif child.tag == 'ul':
				me.add_child( _process_ul_elements( child, epub ) )
			else:
				logger.warn('Unhandled Sidebar child: %s', child)

		return me

class BlockQuote( types.BlockQuote ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child( Paragraph.process( element, epub ) )
		return me

class Image( types.Image ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.path = element.attrib['src']
		if 'alt' in element.attrib.keys():
			me.caption = element.attrib['alt']
		image_path = os.path.join(epub.content_path, me.path)
		if image_path in epub.zipfile.namelist():
			me.data = StringIO( epub.zipfile.read(image_path) )
			me.width, me.height = PILImage.open(me.data).size
			epub.image_list.append(me)
			return me
		else:
			logger.warn("Image Path %s does not exist", image_path)
		
class Video( types.Video ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.path = element.attrib['src']
		me.caption = element.attrib['title']
		me.thumbnail = element.attrib['poster']
		me.thumbnaildata = StringIO( epub.zipfile.read(os.path.join(epub.content_path, me.thumbnail)) )
		#me.width, me.height = PILImage.open(me.thumbnaildata).size
		me.width, me.height = ( 640, 480 )
		me.add_child( Run.process( element, epub ) )
		epub.video_list.append(me)
		return me

class OrderedList( types.OrderedList ):
	
	@classmethod
	def process(cls, element, epub):
		me = cls()
		if 'type' in element.attrib:
			numbering_type = element.attrib['type']
			me.start = 1
			if numbering_type == u'1':
				me.format = 'decimal'
			elif numbering_type == u'a':
				me.format = 'lowerLetter'
			elif numbering_type == u'A':
				me.format = 'upperLetter'
			elif numbering_type == u'i':
				me.format = 'lowerRoman'
			elif numbering_type == u'I':
				me.format = 'upperRoman'
			else:
				logger.warn("UNHANDLED OrderedList numbering format type %s", numbering_type)

		for child in element:
			el = None
			if child.tag == 'li':
				el = Item.process(child, epub)
			else:
				logger.info('OrderedList child %s',child.tag)
				el = Item()

			if isinstance(el, types.Item) or isinstance(el, types.List):
				me.add_child( el )
			else:
				if len(me.children) == 0:
					me.add_child( Item() )
				me.children[-1].add_child( el )

		return me

class UnorderedList( types.UnorderedList ):

	@classmethod
	def process(cls, element, epub):
		me = cls()

		for child in element:
			el = None
			if child.tag == 'li':
				el = Item.process(child, epub)
			elif child.tag == 'div':
				el = _process_div_elements(child, epub)
			elif child.tag == 'p':
				el = _process_p_elements(child, epub)
			else:
				logger.info('undordered list %',child)
				el = Item()

			if isinstance(el, types.Item) or isinstance(el, types.List):
				me.add_child( el )
			else:
				if len(me.children) == 0:
					me.add_child( Item() )
				me.children[-1].add_child( el )

		return me

class DescriptionList( types.DescriptionList ):
	
	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(ItemWithDesc.process(element, epub))
		return me

class ItemWithDesc( types.ItemWithDesc ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		count_child = -1
		for child in element:
			if child.tag == 'dt':
				el = DT.process(child, epub)
				me.add_child(el)
				count_child = count_child + 1
			elif child.tag == 'dd':
				if me.children[count_child].desc == None:
					desc = []
					_dd = DD.process(child, epub)
					desc.append(_dd)
					me.children[count_child].set_description(desc)
				else:
					desc = me.children[count_child].desc
					_dd = DD.process(child, epub)
					desc.append(_dd)
					me.children[count_child].set_description(desc)
			elif child.tag == 'a':
				if me.children[count_child].desc == None:
					desc = []
					_a = _process_a_elements(child, epub)
					desc.append(_a)
					me.children[count_child].set_description(desc)
				else:
					desc = me.children[count_child].desc
					_a = _process_a_elements(child, epub)
					desc.append(_a)
					me.children[count_child].set_description(desc)
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <dl> element child: %s.',child.tag)
		return me

class DT(types.DT):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for sub_el in element:
			if sub_el.tag == 'p':
				me.add_child(_process_p_elements(sub_el, epub))
			elif sub_el.tag == 'img':
				me.add_child(Image.process(sub_el, epub))
			elif sub_el.tag ==  'span':
				me.add_child(_process_span_elements(sub_el, epub))
			elif sub_el.tag ==  'sub':
				me.add_child(_process_sub_elements(sub_el, epub))
			elif sub_el.tag ==  'sup':
				me.add_child(_process_sup_elements(sub_el, epub))
			else:
				if isinstance(sub_el,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <dt> child: %s.',sub_el.tag)
		return me

class DD(types.DD):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for sub_el in element:
			if sub_el.tag == 'p':
				me.add_child(_process_p_elements(sub_el, epub))
			elif sub_el.tag == 'div':
				me.add_child(_process_div_elements(sub_el, epub))
			else:
				if isinstance(sub_el,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <dd> child: %s.',sub_el.tag)
		return me

class Item( types.Item ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for sub_el in element:
			if sub_el.tag == 'ul':
				me.add_child(_process_ul_elements(sub_el, epub))
			elif sub_el.tag == 'a':
				me.add_child(_process_a_elements(sub_el, epub))
			elif sub_el.tag == 'p':
				me.add_child(_process_p_elements(sub_el, epub))
			elif sub_el.tag == 'span':
				me.add_child(_process_span_elements(sub_el, epub))
			elif sub_el.tag == 'div':
				me.add_child(_process_div_elements(sub_el, epub))
			elif sub_el.tag == 'sub':
				me.add_child(_process_sub_elements(sub_el, epub))
			elif sub_el.tag == 'sup':
				me.add_child(_process_sup_elements(sub_el, epub))
			elif sub_el.tag == 'table':
				me.add_child(_process_table_elements(sub_el, epub))
			elif sub_el.tag == 'br':
				me.add_child( types.Newline())
				if sub_el.tail:
					me.add_child(types.TextNode(sub_el.tail))
			else:
				if isinstance(sub_el,HtmlComment):
					pass
				else:
					logger.warn('Unhandled item child: %s.',sub_el.tag)
		return me

class Table(types.Table):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		count_child = -1
		number_of_col = 0
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for child in element:
			if child.tag == 'colgroup':
				me.add_child(_process_colgroup_elements(child, epub))
			elif child.tag == 'tbody':
				me.add_child(_process_tbody_elements(child, epub))
				number_of_col = me.children[count_child].number_of_col
			elif child.tag == 'tr':
				me.add_child(Row.process(child, epub))
			elif child.tag == 'thead':
				me.add_child(THead.process(child, epub))
				number_of_col = me.children[count_child].number_of_col
			elif child.tag == 'tfoot':
				me.add_child(TFoot.process(child, epub))
			elif child.tag == 'caption':
				if child.text:
					me.set_caption(child.text)
					logger.info("Table caption = %s", me.caption)
				count_child = count_child - 1
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled table child: %s.',child.tag)
				count_child = count_child - 1
			count_child = count_child + 1

		me.set_number_of_col(number_of_col)
		return me

class TBody(types.TBody):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0 
		count_child = -1
		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text))
		for child in element:
			if child.tag == 'tr':
				me.add_child(Row.process(child, epub))
				number_of_col = me.children[count_child].number_of_col
				count_child = count_child + 1
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <tbody> child: %s.',child.tag)
		me.set_number_of_col(number_of_col)
		return me

class THead(types.THead):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0 
		count_child = -1
		for child in element:
			if child.tag == 'tr':
				me.add_child(Row.process(child, epub))
				number_of_col = me.children[count_child].number_of_col
				count_child = count_child + 1
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <thead> child: %s.',child.tag)
		me.set_number_of_col(number_of_col)
		return me

class TFoot(types.TFoot):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0 
		count_child = -1
		for child in element:
			if child.tag == 'tr':
				me.add_child(Row.process(child, epub))
				number_of_col = me.children[count_child].number_of_col
				count_child = count_child + 1
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <tfoot> child: %s.',child.tag)
		me.set_number_of_col(number_of_col)
		return me

class Row(types.Row):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0
		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text))
		for child in element:
			if child.tag == 'td' or child.tag == 'th':
				me.add_child(Cell.process(child, epub))
				number_of_col = number_of_col + 1
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <tr> child: %s.',child.tag)
		me.set_number_of_col(number_of_col)
		return me

class Cell(types.Cell):

	@classmethod
	def process(cls, element, epub):
		#logger.info("CHECK cell element")
		me = cls()
		if 'id' in element.attrib:
			me.add_child(Label.process(element, epub))

		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))

		for child in element:
			if child.tag == 'a':
				me.add_child(_process_a_elements(child,epub))
			elif child.tag == 'p':
				me.add_child(_process_p_elements(child, epub))
			elif child.tag == 'br':
				me.add_child( types.Newline())
				if child.tail:
					me.add_child(types.TextNode(child.tail))
			elif child.tag == 'img':
				me.add_child(Image.process(child, epub))
			elif child.tag == 'sub':
				me.add_child(_process_sub_elements(child, epub))
			elif child.tag == 'h4':
				me.add_child(_process_h4_elements(child, epub))
			elif child.tag == 'big':
				me.add_child(_process_big_elements(child, epub))
			elif child.tag == 'span':
				me.add_child( _process_span_elements( child, epub ) )
			elif child.tag == 'div':
				me.add_child(_process_div_elements(child, epub))
			elif child.tag == 'sup':
				me.add_child(_process_sup_elements(child, epub ))
			elif child.tag == 'em':
				me.add_child(_process_em_elements(child, epub))
			elif child.tag == 'table':
				me.add_child(_process_table_elements(child, epub))
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <td> child: %s.',child.tag)
		return me

class CodeLine(types.CodeLine):

	@classmethod
	def process(cls, element, epub):
		#logger.info("CHECK cell element")
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for child in element.iterchildren():
			if child.tag == 'em':
				me.add_child(_process_em_elements(child, epub))
			elif child.tag == 'strong':
				me.add_child(_process_strong_elements(child, epub))
			elif child.tag == 'dfn':
				me.add_child(_process_dfn_elements(child, epub))
			elif child.tag == 'code':
				me.add_child(_process_code_elements(child, epub))
			elif child.tag == 'samp':
				me.add_child(_process_samp_elements(child, epub))
			elif child.tag == 'kbd':
				me.add_child(_process_kbd_elements(child, epub))
			elif child.tag == 'var':
				me.add_child(_process_var_elements(child, epub))
			elif child.tag == 'span':
				me.add_child(_process_span_elements(child, epub))
			elif child.tag == 'sup':
				me.add_child(_process_sup_elements(child, epub))
			else:
				logger.warn('Unhandled <code> element : %s', child.tag)
		return me

class Math(types.Math):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MRow(types.MRow):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		for child in element:
			if child.tag == 'mtable':
				me.add_child(_process_mtable_elements(child, epub))
			elif child.tag == 'mi':
				me.add_child(_process_mi_elements(child, epub))
			elif child.tag == 'mo':
				me.add_child(_process_mo_elements(child, epub))
			elif child.tag == 'mn':
				me.add_child(_process_mn_elements(child, epub))
			elif child.tag == 'mrow':
				me.add_child(_process_mrow_elements(child, epub))
			elif child.tag == 'mfenced':
				me.add_child(_process_mfenced_elements(child, epub))
			elif child.tag == 'mspace':
				pass
			elif child.tag == 'msqrt':
				me.add_child(_process_msqrt_elements(child, epub))
			elif child.tag == 'MRoot':
				me.add_child(_process_MRoot_elements(child, epub))
			elif child.tag == 'msub':
				me.add_child(_process_msub_elements(child, epub))
			elif child.tag == 'msup':
				me.add_child(_process_msup_elements(child, epub))
			elif child.tag == 'MFrac':
				me.add_child(_process_MFrac_elements(child, epub))
			elif child.tag == 'msubsup':
				me.add_child(_process_msubsup_elements(child, epub))
			elif child.tag == 'munderover':
				me.add_child(_process_munderover_elements(child,epub))
			elif child.tag == 'mover':
				me.add_child(_process_mover_elements(child, epub))
			elif child.tag == 'munder':
				me.add_child(_process_munder_elements(child, epub))
			elif child.tag == 'mtext':
				me.add_child(_process_mtext_elements(child, epub))
			else:
				logger.warn('UNHANDLED element found under mrow %s', child.tag)
		return me

class MFenced(types.MFenced):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.close = element.attrib['close']
		me.opener = element.attrib['open']
		me.separators = element.attrib['separators']
		for child in element:
			if child.tag == 'mtable':
				me.add_child(_process_mtable_elements(child, epub))
			elif child.tag == 'mrow':
				me.add_child(_process_mrow_elements(child, epub))
			else:
				me.add_child(MathRun.process(element,epub))
		return me

class Mtable(types.Mtable):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0 
		count_child = -1
		if 'id' in element.attrib:
			me.add_child(Label.process(element, epub))

		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text, type_text = 'omath'))

		for child in element:
			if child.tag == 'mtr':
				me.add_child(_process_mtr_elements(child, epub))
				number_of_col = me.children[count_child].number_of_col 
			else:
				logger.warn("UNHANDLED child under TABLE element %s", child.tag)
			count_child = count_child + 1
		me.set_number_of_col(number_of_col)
		return me

class Mtr(types.Mtr):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		number_of_col = 0
		if 'id' in element.attrib:
			me.add_child(Label.process(element, epub))

		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text, type_text = 'omath'))

		for child in element:
			if child.tag == 'mtd':
				me.add_child(_process_mtd_elements(child, epub))
				number_of_col = number_of_col + 1
			else:
				logger.warn("UNHANDLED child under TABLE element %s", child.tag)
		me.set_number_of_col(number_of_col)
		return me

class Mtd(types.Mtd):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MFrac(types.MFrac):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		if 'id' in element.attrib:
			me.add_child(Label.process(element, epub))

		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text, type_text = 'omath'))

		for child in element:
			if child.tag == 'mrow':
				me.add_child(_process_mrow_elements(child, epub))
			else:
				logger.warn("UNHANDLED child under TABLE element %s", child.tag)
		return me

class MSup(types.MSup):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MSub(types.MSub):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MSubSup(types.MSubSup):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MSqrt(types.Msqrt):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element,epub))
		return me

class MRoot(types.MRoot):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MUnder(types.MUnder):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MUnderover(types.MUnderover):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MOver(types.MOver):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(MathRun.process(element, epub))
		return me

class MathRun(types.MathRun):

	@classmethod
	def process(cls, element, epub, styles=None):
		me = cls()
		styles = styles or []
		me.styles.extend(styles)
		if element.text:
			if element.text.isspace():
				pass
			else:
				me.add_child(types.TextNode(element.text, type_text = 'omath'))
		
		for child in element:
			if child.tag == 'mi':
				me.add_child(_process_mi_elements(child, epub))
			elif child.tag == 'mo':
				me.add_child(_process_mo_elements(child, epub))
			elif child.tag == 'mn':
				me.add_child(_process_mn_elements(child, epub))
			elif child.tag == 'mrow':
				me.add_child(_process_mrow_elements(child, epub))
			elif child.tag == 'msup':
				me.add_child(_process_msup_elements(child, epub))
			elif child.tag == 'msub':
				me.add_child(_process_msub_elements(child,epub))
			elif child.tag == 'mfenced':
				me.add_child(_process_mfenced_elements(child, epub))
			elif child.tag == 'mspace':
				pass
			elif child.tag == 'msubsup':
				me.add_child(_process_msubsup_elements(child, epub))
			elif child.tag == 'MFrac':
				me.add_child(_process_MFrac_elements(child, epub))
			elif child.tag == 'mover':
				me.add_child(_process_mover_elements(child, epub))
			elif child.tag == 'mtable':
				me.add_child(_process_mtable_elements(child, epub))
			elif child.tag == 'msqrt':
				me.add_child(_process_msqrt_elements(child,epub))
			elif child.tag == 'MRoot':
				me.add_child(_process_MRoot_elements(child,epub))
			elif child.tag == 'mtext':
				me.add_child(_process_mtext_elements(child, epub))
			elif child.tag == 'munderover':
				me.add_child(_process_munderover_elements(child, epub))
			elif child.tag == 'munder':
				me.add_child(_process_munder_elements(child,epub))
			elif child.tag == 'mstyle':
				pass
			else:
				logger.warn("UNHANDLED child tag under MathRun.process : %s", child.tag)

		return me

def adapt(fragment, epub, label):

	els = _process_fragment( fragment, epub )

	# Make sure that each chapter and section object have a Label child
	if els and (isinstance(els[0], Chapter) or isinstance(els[0], Section)):
		label_el = Label()
		label_el.name = label
		els[0].add_child( label_el )

	# Upgrade front and back matter 'sections' to 'chapters' as appropriate
	if els and isinstance(els[0], Section):
		if els[0].children[-1].name[0] in [ 'b', 'f' ] and len(els[0].children[-1].name) == 3:
			chapter = Chapter()
			for child in els[0].children:
				chapter.add_child(child)
			els[0] = chapter

	for el in els:
		_fix_hyperlinks( el, epub.manifest )

	return els

def _fix_hyperlinks( element, manifest ):

	if isinstance( element, Hyperlink ):
		hyperparts = urlparse( element.target )
		for item in manifest:
			if hyperparts[2] == manifest[item]['href']:
				element.type = u'Pageref'
				if hyperparts[5]:
					element.target = hyperparts[5]
				else:
					element.target = item
	else:
		if hasattr(element, 'children'):
			for child in element.children:
				_fix_hyperlinks( child, manifest )

def _process_fragment( fragment, epub ):
	head = fragment.find('head')
	body = fragment.find('body')
	el = []
	for element in body:
		if element.tag == 'div':
			el.append(_process_div_elements( element, epub ))
		elif element.tag == 'p':
			el.append(_process_p_elements( element, epub ))
		elif element.tag == 'h1':
			el.append(_process_h1_elements( element, epub ))
		elif element.tag == 'h2':
			el.append(_process_h2_elements( element, epub ))
		elif element.tag == 'h3':
			el.append(_process_h3_elements( element, epub ))
		elif element.tag == 'h4':
			el.append(_process_h4_elements( element, epub ))
		elif element.tag == 'h5':
			el.append(_process_h5_elements( element, epub ))
		elif element.tag == 'ul':
			el.append(_process_ul_elements( element, epub ))
		elif element.tag == 'section':
			el.append(_process_section_elements(element, epub))
		elif element.tag == 'hr':
			el.append(_process_hr_elements(element,epub))
		elif element.tag == 'table':
			el.append(_process_table_elements(element,epub))
		elif element.tag == 'nav':
			el.append(_process_nav_elements(element, epub))
		else:
			logger.warn('on process_fragment UNHANDLED BODY CHILD: %s >> %s',element.tag, element )
	# Consolidate multi-line chapter or section titles
	new_el = []
	for i in range(len(el)):
		if (i+1 < len(el)) and type(el[i]) == type(el[i+1]):
			if type(el[i]) == Chapter or type(el[i]) == Section:
				el[i].add_child( types.TextNode(': ') )
				for child in el[i+1].children:
					el[i].add_child( child )
				el[i+1] = el[i]
			else:
				new_el.append(el[i])
		else:
			new_el.append(el[i])
	el = new_el
	#el2 = el
	# If the chapter or section title was not parsed out of the text, then extract it from the document head.
	# Maybe we should do this all of the time.
	chapter = Chapter()
	chapter.suppressed = True
	#logger.info('_get_title(head) >> %s', _get_title( head ))
	chapter.add_child( types.TextNode( _get_title( head ) ) )
	if el == []:
		#logger.info ('append el')
		el.append(chapter)
	elif not ( (isinstance(el[0], Chapter) or isinstance(el[0], Section)) ):
		#logger.info('el.insert works')
		el.insert(0,chapter)
	el = _consolidate_lists( el )

	return el

def _get_title( head ):
	title = u''
	for element in head:
		if element.tag == 'title':
			title = element.text
	return title

def _consolidate_lists(data=()):

	def pull_up_children( element ):
		if isinstance(element, types.List):
			for i in range(len(element.children)):
				if 	isinstance(element.children[i], types.List) and \
					element.level == element.children[i].level:
					child = element.children[i]
					for j in range(len(child.children)):
						element.children.insert(i+j, child.children[j])
					element.children.remove(child)

	new_list = []
	for i in range(len(data)):
		if	isinstance(data[i], types.List) and \
            (i + 1 < len(data)) and \
            isinstance(data[i+1], types.List) and \
            data[i].group == data[i+1].group:
			if data[i].level == data[i+1].level:
				for child in data[i+1].children:
					data[i].add_child( child )
					data[i+1] = data[i]
			elif data[i].level < data[i+1].level:
				data[i].add_child( data[i+1] )
				data[i+1] = data[i]
			else:
				data[i].children = _consolidate_lists( data[i].children )
				# Pull up children if necessary
				pull_up_children( data[i] )
				new_list.append( data[i] )
		else:
			if isinstance(data[i], types.List):
				data[i].children = _consolidate_lists( data[i].children )
				# Pull up children if necessary
				pull_up_children( data[i] )
			new_list.append( data[i] )
	return new_list

def _process_div_elements( element, epub ):
	#logger.info ('check element atrribute of body: %s', element.attrib.keys())
	#logger.info ('type: ',type(element))
	#class_ = u''
	#el = None
	el = Run.process(element, epub)
	return el

def _process_p_elements( element, epub ):
	el = Paragraph.process(element, epub)
	return el

def _process_section_elements(element, epub):
	el = Paragraph.process(element, epub)
	return el

def _process_h1_elements( element, epub ):
	return SubSection.process(element, epub)

def _process_h2_elements( element, epub ):
	return SubSubSection.process(element, epub)

def _process_h3_elements( element, epub ):
	return Paragraph.process(element, epub, ['Heading3'])

def _process_h4_elements( element, epub ):
	return Paragraph.process(element, epub, ['Heading4'])

def _process_h5_elements( element, epub ):
	return Paragraph.process(element, epub, ['Heading5'])

def _process_h6_elements( element, epub ):
	return Paragraph.process(element, epub, ['Heading6'])

def _process_h7_elements( element, epub ):
	return Paragraph.process(element, epub, ['Heading7'])

def _process_span_elements( element, epub ):
	return Run.process(element, epub)

def _process_ul_elements( element, epub ):
	return UnorderedList.process(element, epub)

def _process_dl_elements( element, epub ):
	return DescriptionList.process(element, epub)

def _process_b_elements( element, epub ):
	return Run.process(element, epub, ['bold'])

def _process_i_elements( element, epub ):
	return Run.process(element, epub, ['italic'])

def _process_sub_elements( element, epub ):
	return Run.process(element, epub, ['sub'])

def _process_sup_elements( element, epub ):
	return Run.process(element, epub, ['sup'])

def _process_a_elements( element, epub ):
	if 'href' in element.attrib.keys():
		el = None
		if element.tail:
			el = Run()
			el.add_child( Hyperlink.process(element, epub) )
			el.add_child( types.TextNode(element.tail))
		else:
			el = Hyperlink.process(element, epub)
		return el
	else:
		el = None
		if element.tail:
			el = Run()
			if 'id' in element.attrib.keys():
				el.add_child( Label.process(element, epub) )
			el.add_child( types.TextNode(element.tail) )
		else:
			if 'id' in element.attrib.keys():
				el = Label.process(element, epub)
	return el

def _process_strong_elements(element, epub):
	return Run.process(element, epub, ['bold'])

def _process_em_elements(element, epub):
	return Run.process(element, epub, ['italic'])

def _process_q_elements(element, epub):
	return Run.process(element, epub, ['bold'])

def _process_dfn_elements(element, epub):
	return Run.process(element, epub, 'italic')

def _process_code_elements(element, epub):
	return CodeLine.process(element,epub)

def _process_samp_elements(element, epub):
	return Run.process(element, epub)

def _process_kbd_elements(element, epub):
	return Run.process(element,epub)

def _process_var_elements(element, epub):
	return Run.process(element, epub, ['italic']) 

def _process_hr_elements(element, epub):
	return Run.process(element, epub)

def _process_big_elements(element, epub):
	return Run.process(element, epub)

def _process_ol_elements(element, epub):
	return OrderedList.process(element, epub)

def _process_table_elements(element, epub):
	return Table.process(element,epub)

def _process_colgroup_elements(element, epub):
	pass

def _process_tbody_elements(element, epub):
	return TBody.process(element, epub)

def _process_tr_elements(element, epub):
	return Row.process(element, epub)

def _process_td_elements(element, epub):
	return Cell.process(element, epub)

def _process_nav_elements(element, epub):
	return Run.process(element, epub)

def _process_math_elements(element, epub):
	return Math.process(element, epub)

def _process_mrow_elements(element,epub):
	return MRow.process(element, epub)

def _process_msup_elements(element,epub):
	return MSup.process(element, epub)

def _process_msub_elements(element, epub):
	return MSub.process(element, epub)

def _process_msubsup_elements(element, epub):
	return MSubSup.process(element, epub)

def _process_mi_elements(element, epub):
	return MathRun.process(element, epub)

def _process_mn_elements(element, epub):
	return MathRun.process(element, epub)

def _process_mo_elements(element, epub):
	return MathRun.process(element, epub)

def _process_mspace_elements(element, epub):
	return MathRun.process(element, epub)

def _process_mfenced_elements(element, epub):
	return MFenced.process(element, epub)

def _process_mtable_elements(element, epub):
	return Mtable.process(element, epub)

def _process_mtr_elements(element, epub):
	return Mtr.process(element, epub)

def _process_mtd_elements(element, epub):
	return Mtd.process(element, epub)

def _process_MFrac_elements(element, epub):
	return MFrac.process(element, epub)

def _process_msqrt_elements(element, epub):
	return MSqrt.process(element, epub)

def _process_MRoot_elements(element, epub):
	return MRoot.process(element, epub)

def _process_munder_elements(element, epub):
	return MUnder.process(element, epub)

def _process_munderover_elements(element, epub):
	return MUnderover.process(element, epub)

def _process_mover_elements(element, epub):
	return MOver.process(element,epub)

def _process_mtext_elements(element, epub):
	return MathRun.process(element, epub)
