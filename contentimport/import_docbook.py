#!/usr/bin/env python2.7

import os
import re
import sys

def first_pass(line):
    # Remove trailing blank comments
    p = re.compile( r'%$' )
    line = p.sub( '', line )

    # Remove extra commands inserted by dblatex
    line = line.replace( r'\begin{abstract}', '' )
    line = line.replace( r'\end{abstract}', '' )

    p = re.compile( r'\\set[a-z]*font{[A-Za-z ]*}' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\\usepackage{[a-z]*}' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\\usepackage\[[A-Za-z0-9]*\]{[a-z]*}' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\\hyperlabel{[A-Za-z0-9_.-]*}' )
    line = p.sub( '', line )

    p = re.compile( r'^pdf[A-Za-z0-9={} .,-]*' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'^\s*}{' + '\n' )
    line = p.sub( '', line )

        #p = re.compile( r'^\s*{|^\s*}' + '\n' )
        #line = p.sub( '', line )
        #line = p.sub( '', line )

    p = re.compile( r'\\hypersetup{' + '\n' )
    line = p.sub( '{', line )

    p = re.compile( r'^\\renew[A-Za-z0-9{}\\]*DBK[A-Za-z0-9{}\\]*}' + '\n')
    line = p.sub( '', line )

    p = re.compile( r'^\\renew[A-Za-z0-9{}\\]*DBK[A-Za-z0-9{}\\]*' + '\n')
    line = p.sub( '{', line )

    p = re.compile( r'^\\[A-Za-z0-9{}\\]*DBK[A-Za-z0-9{}\\]*' + '\n')
    line = p.sub( '', line )

    p = re.compile( r'\\DBKinditem{[A-Za-z0-9\\]*}{[A-Za-z ,]*}' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\\begin{DBKadmonition}{}{[A-Za-z0-9{}:\\\'?!() ,_-]*}' )
    line = p.sub( '', line )

    p = re.compile( r'\\IfFileExists{ifxetex.sty}{' + '\n' )
    line = p.sub( '{', line )

    p = re.compile( r'\s*\\newif\\ifxetex' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\s*\\xetexfalse' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'\s*\\ifxetex' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'^\\else' + '\n' )
    line = p.sub( '', line )

    p = re.compile( r'^\\fi' + '\n' )
    line = p.sub( '', line )

    # Remove excess commands around tables
    p = re.compile( r'\\centering[a-z\\ ]*' )
    line = p.sub( '', line )

    p = re.compile( r'\\setlength[-A-Za-z0-9{}/\\ ]*' + '\n' )
    line = p.sub( '', line )

    line = line.replace( r'\endgroup', '' )
    line = line.replace( r'\restoretablecounter' + '\n', '' )

    return line

def second_pass(line):
    # Change the document class
    p = re.compile( r'(\\documentclass{)[a-z]*(})' )
    line = p.sub( r'\1book\2', line )

    # Add required packages
    p = re.compile( r'\\documentclass' )
    if p.search( line ) is not None:
        line = line + r'\usepackage{graphicx}' + '\n'
        line = line + r'\usepackage{amsmath}' + '\n'
        line = line + r'\usepackage{longtable}' + '\n'
        line = line + r'\usepackage{nti.contentrendering.ntilatexmacros}' + '\n'
        line = line + r'\usepackage{hyperref}' + '\n'

    # Alter table commands
    p = re.compile( r'm{\\newtblstarfactor[A-Za-z0-9+\\ ]*}' )
    line = p.sub( 'l', line )

    line = line.replace( r'\tabularnewline', r'\\' + '\n' )

    # Insert actual fancy quotes
    line = line.replace( r'\textquotedblleft{}', "``" )
    line = line.replace( r'\textquotedblright{}', "''" )

    # Insert actual em-dash
    line = line.replace( r'\textemdash{}', '--' )

    # Fix normal dashes
    line = line.replace( r'-{}', '-' )

    return line

def convert_docbook(lines):
    output = []
    for line in lines:
        line = first_pass(line)
        line = second_pass(line)

        output.append(line)
    return output

if __name__ == '__main__':
        data = []
        # Get the input
        with open( sys.argv[1:][0], 'rb' ) as input:
                data = input.readlines()

        # Process the input
        output = convert_docbook(data)

        # Output the processed data
        for line in output:
                sys.stdout.write(line)
