#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
from six import StringIO

from PIL import Image as PILImage

from nti.contenttools import types

from nti.contenttools.adapters.epub.ifsta import check_element_tail

from nti.contenttools.adapters.epub.ifsta.run import Run
from nti.contenttools.adapters.epub.ifsta.run import process_div_elements


class Image(types.Image):

    @classmethod
    def process(cls, element, inline_image=False, epub=None):
        me = cls()
        path = element.attrib['src']
        if u'../' in path:
            path = path.replace('../', '')
        _, filename = os.path.split(path)
        me.predefined_image_path = True
        me.path = u'Images/CourseAssets/%s/%s' % (epub.book_title, filename)
        me.inline_image = inline_image
        if 'alt' in element.attrib.keys():
            me.caption = types.TextNode(element.attrib['alt'])

        zipfile = epub.zipfile
        image_path = os.path.join(epub.content_path, path)
        if image_path in zipfile.namelist():
            image_data = StringIO(zipfile.read(image_path))
            save_image(image_data, me.path, epub)
            me.width, me.height = PILImage.open(image_data).size
        else:
            logger.warn('COULD NOT FIND Image : %s', image_path)
            return types.Run()

        figures_without_caption = (u'Icon',)
        to_ignore = (u'Divider_Page', u'Warning', u'Caution')

        if any(fig in filename for fig in figures_without_caption):
            figure = Figure()
            title, _ = os.path.splitext(filename)
            figure.centered = False
            figure.floating = True
            figure.icon = True
            me.inline_image = True
            figure.add(me)
            return figure
        elif any(fig in filename for fig in to_ignore):
            return types.Run()
        elif u'-' in filename:
            figure = Figure()
            figure.centered = False
            title, _ = os.path.splitext(filename)
            figure.label = u'fig:%s_%s' % (epub.book_title, title)
            figure.caption = u'%s' % (title.replace('-', '.'))
            figure.add(me)
            figure.data_type = u'ifsta-numbering-fig'
            epub.figures.append(figure)
            epub.figure_labels[figure.caption] = figure.label
            return figure
        elif u'_' in filename:
            me.inline_image = True
            img_node = Run()
            img_node.add(me)
            img_node = check_element_tail(img_node, element)
            return img_node
        else:
            img_node = Run()
            img_node = check_element_tail(img_node, element)
            return img_node


def save_image(image_data, filepath, epub):
    filepath = u'%s/%s' % (epub.output_directory, filepath)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, 'wb') as fp:
        fp.write(image_data.read())


class Figure(types.Figure):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        if u'id' in element.attrib:
            me.label = element.attrib[u'id']
        for child in element:
            if child.tag == u'figcaption':
                me.caption = Run.process(child, epub=epub)
            elif child.tag == u'span':
                if u'data-type' in child.attrib:
                    me.data_type = child.attrib[u'data-type']
                if u'id' in child.attrib:
                    me.image_id = child.attrib[u'id']
                if u'data-alt' in child.attrib:
                    me.image_alt = types.TextNode(child.attrib[u'data-alt'])
                img = get_figure_image(child, epub)
                me.add_child(img)
            elif child.tag == u'figure':
                me.add_child(Figure.process(child, epub))
            elif child.tag == u'div':
                me.add_child(process_div_elements(child, me, epub=epub))
            else:
                logger.warn('Unhandled figure child %s', child.tag)
        return me


def get_figure_image(element, epub=None):
    for child in element:
        if child.tag == u'img':
            return Image.process(child, epub=epub)
