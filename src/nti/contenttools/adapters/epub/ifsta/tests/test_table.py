#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from lxml import html

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

class TestTable(ContentToolsTestCase):
    def test_table(self):
        script = u'<div><table>\
        <tr>\
        <td>A</td>\
        <td>B</td>\
        <td>C</td>\
        </tr>\
        <tr>\
        <td>1</td>\
        <td>2</td>\
        <td>3</td>\
        </tr></table></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\begin{tabular}{ l  l  l }\nA & B & C\\\\\n1 & 2 & 3\\\\\n\n\\end{tabular}\n\\end{table}\n'))
    
    
    def test_table_2(self):
        script = u'<div><table>\
        <tr>\
        <th>Firstname</th>\
        <th>Lastname</th>\
        <th>Age</th>\
        </tr>\
        <tr>\
        <td>Jill</td>\
        <td>Smith</td>\
        <td>50</td>\
        </tr>\
        <tr>\
        <td>Eve</td>\
        <td>Jackson</td>\
        <td>94</td>\
        </tr>\
        </table></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\begin{tabular}{ l  l  l }\nFirstname & Lastname & Age\\\\\nJill & Smith & 50\\\\\nEve & Jackson & 94\\\\\n\n\\end{tabular}\n\\end{table}\n'))