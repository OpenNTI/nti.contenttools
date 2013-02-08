#!/usr/bin/env python2.7
from dbtexmf.dblatex.rawparse import RawLatexParser, RawUtfParser
from dbtexmf.dblatex.texcodec import TexCodec

import os
import sys


def main(args):
	charmap_extn = {
		u'\u20ac'.encode('utf8'): r'\euro ',
		u'\u00bd'.encode('utf8'): r'$\frac{1}{2}$',
		u'\uf020'.encode('utf8'): " ", # 0xef80a0
		u'\uf02c'.encode('utf8'): " ", # 0xef80ac
		u'\uf02f'.encode('utf8'): "/", # 0xef80af
		u'\uf02e'.encode('utf8'): ".",
		u'\uf06c'.encode('utf8'): " ", # 0xef80ac
		u'\u2022'.encode('utf8'): r"*", # 0xe280a2 (bullet)
		u'\u2212'.encode('utf8'): r"-", # 0xe28892
		u'\u2264'.encode('utf8'): r"$\le$", # 0xef89a4
		u'\u2265'.encode('utf8'): r"$\ge$", # 0xef89a5
		u'\u2248'.encode('utf8'): r"$\approx$", # 0xef8988
		u'\u221E'.encode('utf8'): r"$\infty$", # 0xef889e
		u'\u03bc'.encode('utf8'): r'$\mu$', # 0xcebc
		u'\u03A3'.encode('utf8'): r'$\Sigma$', # 0xcEA3
		u'\uf032'.encode('utf8'): r'$\prime$', # 0xef80b2
		u'\u03b1'.encode('utf8'): r'$\alpha$', # 0xceb1
		u'\u03b2'.encode('utf8'): r'$\beta$', # 0xceb2
		u'\u03b3'.encode('utf8'): r'$\gamma$', # 0xceb3
		u'\u03c1'.encode('utf8'): r'$\rho$', # 0xcf81
		u'\u03c3'.encode('utf8'): r'$\sigma$', # 0xcf83
		u'\u00ad'.encode('utf8'): r'', # 0xc2ad (soft hyphen)
		u'\u03A0'.encode('utf8'): r'$\Pi$', # 0xc2A0
		u'\u0394'.encode('utf8'): r'$\Deltae$', # 0xce94
		u'\u00b5'.encode('utf8'): r'$\mu$', # 0xc2ad (soft hyphen)
		# This is actually the CENT SIGN, but in the symbol font
		# it comes in as prime.
		u'\u00a2'.encode('utf8'): r'$\prime$', # 0xc2c2
		}
	TexCodec.charmap.update( charmap_extn )


	lt = RawLatexParser(output_encoding='utf-8')
	ut = RawUtfParser(output_encoding='utf-8')
	with open( args[0], 'rb' ) as f:
		for line in f.readlines():
			#line = unicode(line)

			line = line.replace( "&#880;", u'\u0370'.encode('utf8') )
			line = line.replace( "&#881;", u'\u0371'.encode('utf8') )
			line = line.replace( "&#8220;", u"\u201c".encode('utf8') )
			line = line.replace( "&#8221;", u"\u201d".encode('utf8') )
			line = line.replace( "&#8217;", u"\u2019".encode('utf8') )
			line = line.replace( "&#8212;", u"\u2014".encode('utf8') )
			line = line.replace( "&#8211;", u"\u2013".encode('utf8') )

			line = line.replace( u'\uf028'.encode("utf8"), '(' )
			line = line.replace( u'\uf029'.encode("utf8"), ')' )
			line = line.replace( u'\u2032'.encode('utf8'), "'" )

			line = line.replace( r"\hyperlabel", r"\label" )

			line = ut.parse( lt.parse( line ) )

			line = line.replace( u"\u00A0".encode('utf8'), " " )
			line = line.replace( u"\u00A9".encode('utf8'), "\copyright" )
			line = line.replace( u"\u201c".encode('utf8'), "``" )
			line = line.replace( u"\u00A7".encode('utf8'), '\\S' )
			line = line.replace( u"\u201d".encode('utf8'), "''" )
			line = line.replace( u"\u2019".encode('utf8'), "'" )
			line = line.replace( u"\u2018".encode('utf8'), "`" )
			line = line.replace( u"\u2014".encode('utf8'), "---" )
			line = line.replace( u"\u2013".encode('utf8'), "--" )
			line = line.replace( u"\227".encode('utf8'), "--" )

			# Math Symbols
			line = line.replace( u"\u2212".encode('utf8'), "$-$" )
			line = line.replace( u"\u221A".encode('utf8'), "$\\sqrt{}$" )
			line = line.replace( u"\u223C".encode('utf8'), "$\\tilde$" )
			line = line.replace( u"\u2248".encode('utf8'), "$\\approx$" )

			# Greek Math Symbols
			line = line.replace( u"\u03B1".encode('utf8'), "$\\alpha$" )
			line = line.replace( u"\u03B2".encode('utf8'), "$\\beta$" )
			line = line.replace( u"\u03BC".encode('utf8'), "$\\mu$" )
			line = line.replace( u"\u03C3".encode('utf8'), "$\\sigma$" )

			# For some ungodly reason, this conversion renders = as a provate use char...
			line = line.replace( u'\uf03d'.encode('utf8'), '=' )
			line = line.replace( u'\uf02d'.encode('utf8'), '-' )
			# likewise with sigma?
			line = line.replace( u'\uf053'.encode('utf8'), r"$\sigma$" )

			# Euro
			line = line.replace( u'\u20ac'.encode('utf8'), r'\euro' )

			# Pound Sterling
			line = line.replace( u'\u00A3'.encode('utf8'), r'\pounds' )

			# MathJax seems to not support \ensuremath, which is
			# the much better thing here.
			line = line.replace( u"\xF7".encode('utf8'), r"$//$" )
			line = line.replace( u"\xD7".encode('utf8'), r"$\times$" )
			line = line.replace( u"\xB5".encode('utf8'), r"" )
			line = line.replace( "\xC2", r"" )
			# graphics
			line = line.replace( '.jpg.jpg', '.jpg' )
			line = line.replace( '.png.png', '.png' )
			line = line.replace( "embedded:graphics", "embedded/graphics" )
			line = line.replace( "embedded:", "embedded/graphics202" )
			print line,

if __name__ == '__main__':
	main( sys.argv[1:] )
