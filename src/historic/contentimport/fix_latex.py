#!/usr/bin/env python2.7
from dbtexmf.dblatex.rawparse import RawLatexParser, RawUtfParser
from dbtexmf.dblatex.texcodec import TexCodec

import os
import re
import sys


def fix_latex(data):
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


	output = []
	lt = RawLatexParser(output_encoding='utf-8')
	ut = RawUtfParser(output_encoding='utf-8')

	for line in data:

		# Remove unsupported meta tags
		p = re.compile( r'\\hyperlabel{[A-Za-z0-9_.]*}' )
		line = p.sub( '', line )

		p = re.compile( r'\\makeindex' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\makeglossary' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\maketitle' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\frontmatter' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\tableofcontents' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\mainmatter' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\lstsetup' + '\n' )
		line = p.sub( '', line )

		p = re.compile( r'\\listoffigures' + '\n' )
		line = p.sub( '', line )

		line = ut.parse( lt.parse( line ) )
		
		line = line.replace( u"|copyright|".encode('utf8'), r"\copyright" )
		line = line.replace( u"|ldots|".encode('utf8'), r"\ldots" )
			
		# Math Symbols
		line = line.replace( u"|cdots|".encode('utf8'), r"$\cdot" )
		line = line.replace( u"|times|".encode('utf8'), r"$\times$" )
		line = line.replace( u"|div|".encode('utf8'), r"$\div$" )
		line = line.replace( u"|-|".encode('utf8'), r"$-$" )
		line = line.replace( u"|pm|".encode('utf8'), r"$\pm$" )
		line = line.replace( u"|sqrt|".encode('utf8'), r"$\sqrt{}$" )
		line = line.replace( u"|tilde|".encode('utf8'), r"\~" )
		line = line.replace( u"|approx|".encode('utf8'), r"$\approx$" )

		# Greek Math Symbols
		line = line.replace( u"|Delta|".encode('utf8'), r"$\Delta$" )
		line = line.replace( u"|Zeta|".encode('utf8'), r"$Z$" )
		line = line.replace( u"|alpha|".encode('utf8'), r"$\alpha$" )
		line = line.replace( u"|beta|".encode('utf8'), r"$\beta$" )
		line = line.replace( u"|gamma|".encode('utf8'), r"$\gamma$" )
		line = line.replace( u"|delta|".encode('utf8'), r"$\delta$" )
		line = line.replace( u"|epsilon|".encode('utf8'), r"$\epsilon$" )
		line = line.replace( u"|mu|".encode('utf8'), r"$\mu$" )
		line = line.replace( u"|sigma|".encode('utf8'), r"$\sigma$" )
		line = line.replace( u"|phi|".encode('utf8'), r"$\phi$" )
		line = line.replace( u"|varphi|".encode('utf8'), r"$\varphi$" )

		# For some ungodly reason, this conversion renders = as a provate use char...
		line = line.replace( u'\uf03d'.encode('utf8'), '=' )
		line = line.replace( u'\uf02d'.encode('utf8'), '-' )
		# likewise with sigma?
		line = line.replace( u'\uf053'.encode('utf8'), r"$\sigma$" )

		# Euro
		line = line.replace( u'|euro|'.encode('utf8'), r'\euro' )

		# Pound Sterling
		line = line.replace( u'|pounds|'.encode('utf8'), r'\pounds' )

		# MathJax seems to not support \ensuremath, which is
		# the much better thing here.
		line = line.replace( u"\xF7".encode('utf8'), r"$//$" )
		line = line.replace( u"\xD7".encode('utf8'), r"$\times$" )
		line = line.replace( u"\xB5".encode('utf8'), r"" )
		line = line.replace( "\xC2", r"" )
		# graphics
		line = line.replace( '.jpg.jpg', '' )
		line = line.replace( '.png.png', '' )
		line = line.replace( '.jpg', '' )
		line = line.replace( '.png', '' )
		line = line.replace( "embedded:graphics", "embedded/image" )
		line = line.replace( "embedded:", "embedded/graphics202" )

		p = re.compile( r'width=[0-9.]*inch,height=[0-9.]*inch,' )
		if p.search( line ) != None:
			line = line.replace( 'inch,', 'in,' )

		output.append(line)
	
	return output

if __name__ == '__main__':
        data = []
        # Get the input
	with open( sys.argv[1:][0], 'rb' ) as input:
                data = input.readlines()

        # Process the input
	output = fix_latex(data)

        # Output the processed data
        for line in output:
                sys.stdout.write(line)
