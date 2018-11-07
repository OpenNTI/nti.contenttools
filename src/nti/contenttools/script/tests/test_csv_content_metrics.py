#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import os

from collections import namedtuple, OrderedDict

from hamcrest import is_not
from hamcrest import has_items
from hamcrest import assert_that

from nti.contenttools.script.csv_content_metrics import read_json
from nti.contenttools.script.csv_content_metrics import read_xml
from nti.contenttools.script.csv_content_metrics import process_data
from nti.contenttools.script.csv_content_metrics import write_to_csv
from nti.contenttools.script.csv_content_metrics import output_csv

from nti.contenttools.tests import ContentToolsTestCase

class TestCSVContentMetrics(ContentToolsTestCase):
    def data_file(self, name):
        return os.path.join(os.path.dirname(__file__), 'data', name)

    def test_process_data(self):
        data  = read_json(self.data_file('content_metrics.json'))
        root = read_xml(self.data_file('eclipse-toc.xml'))
        
        tup = namedtuple('tup', ['title', 'block', 'minutes', 'total_words'])
        data_csv = OrderedDict()

        block = 15
        wpm = 200

        process_data(data, root, block, wpm, tup, data_csv)

        assert_that(data_csv, is_not(None))
        assert_that(data_csv, has_items('tag:nextthought.com,2011-10:IFSTA-HTML-sample_book.sample_book'))
        assert_that(data_csv, has_items('tag:nextthought.com,2011-10:IFSTA-HTML-sample_book.chapter:1'))
        assert_that(data_csv, has_items('tag:nextthought.com,2011-10:IFSTA-HTML-sample_book.section:1'))

        output = output_csv(root.attrib['label'])
        output = self.data_file(output)
        write_to_csv(data_csv, output, ('NTIID', 'Title', 'Block', 'Minutes', 'Total Words'))