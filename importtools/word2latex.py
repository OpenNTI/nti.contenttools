#!/usr/bin/python

import sys 
import os
import codecs

from docx.read import DocxFile
import renders.LaTeX

def main():
	# Get input and output file
	try:
		inputfile = sys.argv[1]
		# Check to see if the file exists
		if not os.path.exists(inputfile):
			print 'Error: Unable to locate input file'
			exit()
		# Check to see if the file is a docx file
		basename = os.path.basename(inputfile)
		fileext = basename.split('.')[len(basename.split('.'))-1]
		if fileext != 'docx':
			print 'Error: Invalid input file. word2lyx only supports docx files.'
			exit()
		outputfile = sys.argv[2]

	# If there is an error encoutered, return general error message
	except:
		print 'Encountered an error opening the file' 
		exit()


	# Open document from input string
	print "Beginning Conversion of " + inputfile

	docxFile = DocxFile( inputfile )
	with codecs.open( outputfile, 'w', 'utf-8' ) as file:
		file.write( docxFile.render() )

	# Copy Document Images to Subfolder
	img_exportfolder = os.path.join(os.path.abspath(os.path.dirname(outputfile)), docxFile.image_dir)
	docxFile.get_images( img_exportfolder )
	
	print 'Conversion successful, output written to ' + outputfile

if __name__ == '__main__': # pragma: no cover
	main()
