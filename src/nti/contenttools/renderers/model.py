#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from six import StringIO

from zope import interface

from nti.contenttools.renderers.interfaces import IRenderContext

from nti.schema.schema import SchemaConfigured

from nti.schema.fieldproperty import createFieldProperties


class RenderContextMixin(object):

    def __init__(self, *args, **kwargs):
        super(RenderContextMixin, self).__init__(*args, **kwargs)
        self.properties = dict()

    def set(self, name, value):
        self.properties[name] = value

    def get(self, name, default=None):
        return self.properties.get(name, default)


@interface.implementer(IRenderContext)
class DefaultRendererContext(SchemaConfigured, RenderContextMixin):
    createFieldProperties(IRenderContext)

    def __init__(self, *args, **kwargs):
        super(DefaultRendererContext, self).__init__(*args, **kwargs)
        self.data = StringIO()

    def write(self, data):
        if data is not None:
            self.data.write(data)
            return True
        return False

    def reset(self):
        self.data.seek(0)

    def read(self):
        self.reset()
        return self.data.read()
