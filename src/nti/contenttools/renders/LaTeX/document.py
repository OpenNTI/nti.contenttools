from .base import base_renderer

def document_renderer(self):
    output = ''
    output = _document_class( self.doc_type )
    for package in self.packages:
        output = output + _use_package( package )
    if self.title:
        output = output + _title( self.title )
    if self.author:
        output = output + _author( self.author )
    output = output + base_renderer(self)
    return output

def _document_class( docclass, options='' ):
    if options:
        options = u'[%s]' % options
    return u'\\documentclass%s{%s}\n' % (options, docclass)

def _use_package( package, options='' ):
    if options:
        options = u'[%s]' % options
    return u'\\usepackage%s{%s}\n' % (options, package)

def _title( title ):
    return u'\\title{%s}\n' % title

def _author( author ):
    return u'\\author{%s}\n' % author
