#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import unittest
from nti.contenttools.glossary import tex_to_json

class TestTexToJson(unittest.TestCase):
	def test_get_key(self):
		pattern = [u'textbf']
		open_token = u'{'
		close_token = u'}'
		string = u'\\textbf{systemic}\\textbf{ circuit }blood flow to and from virtually all of the tissues of the body '
		result = tex_to_json.get_key(string, open_token, close_token, pattern)
		test = u'systemic circuit'
		self.assertEqual(result, test)

		string = u'\\textbf{ventricle }one of the primary pumping chambers of the heart located in the lower portion of the heart; the left ventricle is the major pumping chamber on the lower left side of the heart that ejects blood into the systemic circuit via the aorta and receives blood from the left atrium; the right ventricle is the major pumping chamber on the lower right side of the heart that ejects blood into the pulmonary circuit via the pulmonary trunk and receives blood from the right atrium'
		result = tex_to_json.get_key(string, open_token, close_token, pattern)
		test = u'ventricle'
		self.assertEqual(result, test)

		pattern = [u'textit']
		string = u'\\textit{pulmonary}\\textit{ circuit }blood flow to and from the lungs'
		result = tex_to_json.get_key(string, open_token, close_token, pattern)
		test = u'pulmonary circuit'
		self.assertEqual(result, test)

		pattern = [u'textbf', u'textit']
		string = u'\\textbf{\\textit{pulmonary circuit}}blood flow to and from the lungs'
		result = tex_to_json.get_key(string, open_token, close_token, pattern)
		test = u'pulmonary circuit'
		self.assertEqual(result, test)

		pattern = [u'textit', u'textbf']
		string = u'\\textit{\\textbf{pulmonary circuit}}blood flow to and from the lungs'
		result = tex_to_json.get_key(string, open_token, close_token, pattern)
		test = u'pulmonary circuit'
		self.assertEqual(result, test)

	def test_map_key_value_tex(self):
		pattern = [u'textbf']
		open_token = u'{'
		close_token = u'}'
		content = [	'\\textbf{bicuspid}\\textbf{ valve }(also, mitral valve or left atrioventricular valve) valve located between the left atrium and ventricle; consists of two flaps of tissue\n', 
					'\\textbf{right}\\textbf{ atrioventricular valve }(also, tricuspid valve) valve located between the right atrium and ventricle; consists of three flaps of tissue\n', 
					'\\textbf{coronary arteries }branches of the ascending aorta that supply blood to the heart; the left coronary artery fee ds the left side of the heart, the left atrium and ventricle, and the interventricular septum; the right coronary artery feeds the right atrium, portions of both ventricles, and the heart conduction system\n', 
					'\\textbf{pericardial}\\textbf{ cavity }cavity surrounding the heart filled with a lubricating serous fluid that reduces friction as the heart contracts\n', 
					'\\textbf{pulmonary}\\textbf{ circuit }blood flow to and from the lungs']
		result = tex_to_json.map_key_value_tex(content, pattern, open_token, close_token)
		test_dict = {u'bicuspid valve': u'(also, mitral valve or left atrioventricular valve) valve located between the left atrium and ventricle; consists of two flaps of tissue', 
					 u'right atrioventricular valve': u'(also, tricuspid valve) valve located between the right atrium and ventricle; consists of three flaps of tissue', 
					 u'coronary arteries': u'branches of the ascending aorta that supply blood to the heart; the left coronary artery fee ds the left side of the heart, the left atrium and ventricle, and the interventricular septum; the right coronary artery feeds the right atrium, portions of both ventricles, and the heart conduction system', 
					 u'pericardial cavity': u'cavity surrounding the heart filled with a lubricating serous fluid that reduces friction as the heart contracts', 
					 u'pulmonary circuit': u'blood flow to and from the lungs',
					}
		self.assertEqual(result, test_dict)




