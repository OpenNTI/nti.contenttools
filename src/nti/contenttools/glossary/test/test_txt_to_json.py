#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import unittest
from nti.contenttools.glossary import txt_to_json

class TestTxtToJson(unittest.TestCase):
	def test_map_key_value(self):
		content = [ 'afterload: force the ventricles must develop to effectively pump blood against the resistance in the vessels\n',
		 			'artificial: pacemaker medical device that transmits electrical signals to the heart to ensure that it contracts and pumps blood to the body\n',
		 			'atrioventricular bundle: (also, bundle of His) group of specialized myocardial conductile cells that transmit the impulse from the AV node through the interventricular septum; form the left and right atrioventricular bundle branches\n',
		 			'atrioventricular bundle branches: (also, left or right bundle branches) specialized myocardial conductile cells that arise from the bifurcation of the atrioventricular bundle and pass through the interventricular septum; lead to the Purkinje fibers and also to the right papillary muscle via the moderator band\n',
		 			'atrioventricular (AV) node: clump of myocardial cells located in the inferior portion of the right atrium within the atrioventricular septum; receives the impulse from the SA node, pauses, and then transmits it into specialized conducting cells within the interventricular septum'
		 			]
		token = u':'
		test_dict = {'artificial': 'pacemaker medical device that transmits electrical signals to the heart to ensure that it contracts and pumps blood to the body', 
					 'atrioventricular (AV) node': 'clump of myocardial cells located in the inferior portion of the right atrium within the atrioventricular septum; receives the impulse from the SA node, pauses, and then transmits it into specialized conducting cells within the interventricular septum', 
					 'atrioventricular bundle branches': '(also, left or right bundle branches) specialized myocardial conductile cells that arise from the bifurcation of the atrioventricular bundle and pass through the interventricular septum; lead to the Purkinje fibers and also to the right papillary muscle via the moderator band', 
					 'afterload': 'force the ventricles must develop to effectively pump blood against the resistance in the vessels', 
					 'atrioventricular bundle': '(also, bundle of His) group of specialized myocardial conductile cells that transmit the impulse from the AV node through the interventricular septum; form the left and right atrioventricular bundle branches'
					 }
		result = txt_to_json.map_key_value(content, token)
		self.assertEqual(result, test_dict)

		content = [ 'afterload >> force the ventricles must develop to effectively pump blood against the resistance in the vessels\n',
		 			'artificial >> pacemaker medical device that transmits electrical signals to the heart to ensure that it contracts and pumps blood to the body\n',
		 			'atrioventricular bundle >> (also, bundle of His) group of specialized myocardial conductile cells that transmit the impulse from the AV node through the interventricular septum; form the left and right atrioventricular bundle branches\n',
		 			'atrioventricular bundle branches >> (also, left or right bundle branches) specialized myocardial conductile cells that arise from the bifurcation of the atrioventricular bundle and pass through the interventricular septum; lead to the Purkinje fibers and also to the right papillary muscle via the moderator band\n',
		 			'atrioventricular (AV) node >> clump of myocardial cells located in the inferior portion of the right atrium within the atrioventricular septum; receives the impulse from the SA node, pauses, and then transmits it into specialized conducting cells within the interventricular septum'
		 			]
		token = u'>>'
		result = txt_to_json.map_key_value(content, token)
		self.assertEqual(result, test_dict)
		self.assertEqual(sorted(result, key=lambda key: result[key]), sorted(test_dict, key=lambda key: test_dict[key]))