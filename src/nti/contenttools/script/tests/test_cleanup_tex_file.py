#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.tests import ContentToolsTestCase

from nti.contenttools.script.cleanup_tex_file import change_figure_to_ntiimagecollection_env
from nti.contenttools.script.cleanup_tex_file import update_image_with_aspect_ratio
from nti.contenttools.script.cleanup_tex_file import set_image_to_default_size
from nti.contenttools.script.cleanup_tex_file import cleanup_subsubsection


class TestCleanupTexFile(ContentToolsTestCase):

	def test_change_figure_to_ntiimagecollection_env(self):
		text = u""" In today's world, a new and emerging problem is clandestine laboratories and illegal or legal grow operations. These laboratories may be\textbf{ }located in any occupancy or location, including vehicles, campgrounds, and hotel rooms. These labs may be haphazardly assembled and are often booby trapped. 

\\begin{figure}[]
\\ntiincludeannotationgraphics[width=650.0px,height=449px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-1.png}
\\caption{The risk to responders increases as they move closer to the hazardous material. It is much safer to identify a material from a distance based on a container shape than it is to physically sample the substance with a detection device.}
\\label{fig:Chapter2_HMFR_reflow_2-1}
\\end{figure}
\\

\\begin{figure}[]
\\ntiincludeannotationgraphics[width=650.0px,height=433px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}
\\caption{First responders could have difficulty knowing what an unmarked truck without placards is transporting. \textit{Courtesy of Rich Mahaney.}}
\\label{fig:Chapter2_HMFR_reflow_2-2}
\\end{figure}
\\ \\realpagenumber{47}"""

		expected_text = u""" In today's world, a new and emerging problem is clandestine laboratories and illegal or legal grow operations. These laboratories may be\textbf{ }located in any occupancy or location, including vehicles, campgrounds, and hotel rooms. These labs may be haphazardly assembled and are often booby trapped. 

\\begin{ntiimagecollection}<>
\\ntiincludeannotationgraphics[width=650.0px,height=449px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-1.png}
\\ntidescription{The risk to responders increases as they move closer to the hazardous material. It is much safer to identify a material from a distance based on a container shape than it is to physically sample the substance with a detection device.}
\\label{fig:Chapter2_HMFR_reflow_2-1}
\\end{ntiimagecollection}
\\

\\begin{ntiimagecollection}<>
\\ntiincludeannotationgraphics[width=650.0px,height=433px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}
\\ntidescription{First responders could have difficulty knowing what an unmarked truck without placards is transporting. \textit{Courtesy of Rich Mahaney.}}
\\label{fig:Chapter2_HMFR_reflow_2-2}
\\end{ntiimagecollection}
\\ \\realpagenumber{47}"""

		new_text = change_figure_to_ntiimagecollection_env(text)
		assert_that(new_text, is_(expected_text))
		assert_that(len(new_text), is_(len(expected_text)))

	def test_update_image_with_aspect_ratio(self):
		text = u"""\\ntiincludeannotationgraphics[width=650px,height=433px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		expected_text = u"""\\ntiincludeannotationgraphics[width=617px,height=411px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""

		new_text = update_image_with_aspect_ratio(text, 0.95)
		assert_that(new_text, is_(expected_text))
		assert_that(len(new_text), is_(len(expected_text)))

		text2 = u"""\\ntiincludeannotationgraphics[width=650.0px,height=433.0px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		expected_text2 = u"""\\ntiincludeannotationgraphics[width=617px,height=411px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		new_text2 = update_image_with_aspect_ratio(text2, 0.95)
		assert_that(new_text2, is_(expected_text2))
		assert_that(len(new_text2), is_(len(expected_text2)))

	def test_set_image_to_default_size(self):
		text = u"""\\ntiincludeannotationgraphics[width=650px,height=433px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		expected_text = u"""\\ntiincludeannotationgraphics[width=300px, height=300px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""

		new_text = set_image_to_default_size(text, 300, 300)
		assert_that(new_text, is_(expected_text))
		assert_that(len(new_text), is_(len(expected_text)))

		text2 = u"""\\ntiincludeannotationgraphics[width=650.0px,height=433.0px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		expected_text2 = u"""\\ntiincludeannotationgraphics[width=300px, height=300px]{Images/CourseAssets/Chapter2_HMFR_reflow/2-2.jpg}"""
		
		new_text2 = set_image_to_default_size(text2, 300, 300)
		assert_that(new_text2, is_(expected_text2))
		assert_that(len(new_text2), is_(len(expected_text2)))


	def test_cleanup_subsubsection(self):
		text = u"""\\subsubsection{This is Subsubsection}\\\\"""
		expected_text = u"""\\subsubsection{This is Subsubsection}"""

		new_text = cleanup_subsubsection(text)
		assert_that(new_text, is_(expected_text))
		assert_that(len(new_text), is_(len(expected_text)))

