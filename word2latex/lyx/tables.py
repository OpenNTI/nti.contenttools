#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).

# This file contains data classes and methods used for creating LyX tables

# Global Variables

# Units of measurement supported in Microsoft Word Documents
WORD_UNITS = {'pct':'', 'dxa':'', 'nil':'', 'auto':''}
# 'pct' : fifties of a percent
# 'dxa' : twenties of a point
# 'nil' : no width specified
# 'auto' : automatically determinedf
LYXCELL_BORDERS = {'bottomline':'bottom', 'topline':'top', 
	'leftline':'left', 'rightline':'right'}
	

class lyxTable:
	'''Data structure used to store table data and properties.'''

	def __init__(self):
		self.tabularvalignment = 'middle'
		self.numRows = 0
		self.numColumns = 0
		self.columns = []
		self.rows = []
		self.borders = lyxTableBorders('table')
		self.width = '0'
		self.units = 'unknown'


class lyxTableCol:
	'''Data structure to store table column properties'''

	def __init__(self):
		self.alignment = 'center'	# Text Alignment: left, right, center
		self.valignment = 'top'	# Vertical Alignment: top, bottom, middle
		self.width = '0'
		self.units = None


class lyxTableRow:
	'''Data structure to store table row properties and data. The lyxTableRow is 
		the primary structure used to create the table layout.'''

	def __init__(self):
		self.tableCells = []


class lyxTableCell:
	'''Data structure to store table cell data and properties'''

	def __init__(self):
		# Alignment Properties
		self.textalign = 'left'		# Text Alignment: left, right, center
		self.valignment = None 		# Vertical Alignment: top, bottom, middle
		self.usebox = 'none'		
		self.width = None			# Cell Width
		self.units = None			# Units used for measurements
		self.data = ''				# Contents of the table cell
		self.borders = lyxTableBorders() # Borders of the table cell
		self.span_multicol = 'false'
		self.multicol = '0'
		self.span_multirow = 'false'
		self.multirow_start = 'false'


class lyxTableBorders:
	'''Structure with contains data about the borders for the table or cell'''
	def __init__(self, type='cell'):
		self.type = 'cell'
		self.data = {}
		borders = ('top', 'bottom', 'right', 'left', 'insideH', 'insideV')
		for border in borders:
			self.data[border] = 'unknown'


def word2lyxTableUnits(size, units):
	'''Converts the units used in Microsoft Word documents (pct, dxa, nil, auto) 
		to appropriate LyX units. pct is converted to %textwidth. dxa to points. 
		nil and auto set the column width to 0.'''

	if units == 'pct':
		size = float(float(size)/2)
		return str(size)+'%textwidth'
	elif units == 'dxa':
		size = float(float(size)/20)
		return str(size)+'pt'
	elif units == 'auto':
		return str(0)
	elif units == 'nil':
		return str(0)


def createCellBorder(lyx_table, table_cell, row, col):
	'''Reads the cell border information and writes the appropriate LyX <cell> 
		properties. Uses row and column to determine how the table and cell 
		border properties should be applied. Table border properties are applied 
		first and cell border properties overwrite them if different.'''

	# Create a dictionary of the four potential border values for each cell
	cell_borders = {'bottomline':'', 'topline':'', 'leftline':'', 'rightline':''}

	# Look at the table border settings

	# Check to see if the cell is in the first row of the table, but not the corner
	# lyxTable.borders.data['top'] applies
	if row == 0:
		if lyx_table.borders.data['top'] != 'none':
			cell_borders['topline'] = lyx_table.borders.data['top']
		if lyx_table.borders.data['insideH'] != 'none':
			cell_borders['bottomline'] = lyx_table.borders.data['insideH']

	# Check to see if the cell is in the last row of the table
	# lyxTable.borders.data['bottom'] applies
	elif row == lyx_table.numRows-1:
		if lyx_table.borders.data['bottom'] != 'none':
			cell_borders['bottomline'] = lyx_table.borders.data['bottom']
		if lyx_table.borders.data['insideH'] != 'none':
			cell_borders['topline'] = lyx_table.borders.data['insideH']

	# Check to see if the cell is in the interior parts of the table
	# (not the first or last row, not the first or last column)
	# lyxTable.borders.data['insideV'] and lyxTable.borders.data['insideH'] apply
	if ((row > 0) & (row < lyx_table.numRows-1)) & \
		((col > 0) & (col < lyx_table.numColumns-1)):
		cell_borders['bottomline'] = lyx_table.borders.data['insideH']
		cell_borders['topline'] = lyx_table.borders.data['insideH']
		cell_borders['leftline'] = lyx_table.borders.data['insideV']
		cell_borders['rightline'] = lyx_table.borders.data['insideV']

	# Check to see if the cell is in the first column of the table
	# lyxTable.borders.data['left'] and applies
	if col == 0:
		if lyx_table.borders.data['left'] != 'none':
			cell_borders['leftline'] = lyx_table.borders.data['left']
		if lyx_table.borders.data['insideV'] != 'none':
			cell_borders['rightline'] = lyx_table.borders.data['insideV']

	# Check to see if the cell is in the last column of the table
	# lyxTable.borders.data['right'] applies
	elif col == lyx_table.numColumns-1:
		if lyx_table.borders.data['right'] != 'none':
			cell_borders['rightline'] = lyx_table.borders.data['right']
		if lyx_table.borders.data['insideV'] != 'none':
			cell_borders['leftline'] = lyx_table.borders.data['insideV']

	# Iterate through cell_borders and write the LyX document values to return
	docstring_borders = u''
	for border in cell_borders:

		# Compare the value to what is in the tableCell
		# if different, overwrite writh the value from the tableCell
		if (table_cell.borders.data[LYXCELL_BORDERS[border]] != 'unknown') \
			& (cell_borders[border] != table_cell.borders.data[LYXCELL_BORDERS[border]]) \
			& (table_cell.borders.data[LYXCELL_BORDERS[border]] != 'unknown'):
			
			cell_borders[border] = table_cell.borders.data[LYXCELL_BORDERS[border]]

			# Translate from Word Options to LyX Options
			if cell_borders[border] == 'nil':
				cell_borders[border] = 'false'
			if cell_borders[border] == 'single':
				cell_borders[border] = 'true'

		if cell_borders[border] == 'true':
			docstring_borders = docstring_borders + ' ' + border + '="' \
				+ cell_borders[border] + '" '

	return docstring_borders


def writeLyxTable(lyx_table):
	'''Parses a lyxTable class to markup that can be written to file.'''
	
	table_header = u'\\begin_inset Tabular\n<lyxtabular version="3" rows="' \
		+ str(lyx_table.numRows) + '" columns="' \
		+ str(lyx_table.numColumns) + '">\n'

	table_foot = '</lyxtabular>\n\\end_inset\n'
	table_output = u''
	row = 0

	# Copy Table Units to Coluns
	for table_col in lyx_table.columns:
		table_col.units = lyx_table.units

	# Create representation of table rows and cells
	for table_row in lyx_table.rows:
		row_output = '<row>\n'
		col = 0
		
		# Create markup for table cells
		for table_cell in table_row.tableCells:
			# If cell spans multiple columns, create entry
			multicol_output = u''
			if table_cell.span_multicol == 'true': multicol_output = 'multicolumn="1" '

			# If cell spans multiple rows, create entry
			multirow_output = u''
			if table_cell.span_multirow == 'true':
				if table_cell.multirow_start != 'false':
					multirow_output = 'multirow="3" '
				else:
					multirow_output = 'multirow="4" '

			# Write table cell settingss
			cell_output = '<cell ' + multicol_output + multirow_output + 'alignment="' \
				+ table_cell.textalign.lower() + '"' \
				+ createCellBorder(lyx_table, table_cell, row, col) \
				+ 'usebox="' + table_cell.usebox.lower() + '">\n'
			cell_output = cell_output + table_cell.data + '</cell>\n'

			# If the cell spans multiple columns, create dummy cells
			if table_cell.span_multicol == 'true':
				for dummy_cell in range(1, int(table_cell.multicol)):
					col = col + 1
					cell_output = cell_output + '<cell multicolumn="2" alignment="' \
						+ table_cell.textalign.lower() + '"' \
						+ createCellBorder(lyx_table, table_cell, row, col) \
						+ 'usebox="' + table_cell.usebox.lower() + '">\n' \
						+ '\\begin_inset Text\n' \
						+ '\\begin_layout\n' + '\\end_layout\n\\end_inset\n</cell>\n'

			# Append the cell output to the row output
			row_output = row_output + cell_output

			if table_cell.span_multicol != 'true':
				# Compare column properties to cell properties, adjust if needed
				table_col = lyx_table.columns[col]
				# Check to see if the width of the table column has been assigned units
				# if not, use the units of the cell
				if (table_col.units == None) | (table_col.units != table_cell.units):
						table_col.units = table_cell.units
				# Adjust column width so that it matches the width of largest cell
				if float(table_cell.width) >= float(table_col.width):
					table_col.width = table_cell.width
				lyx_table.columns[col] = table_col
			
			col = col + 1

		table_output = table_output + row_output + '</row>\n'
		row = row + 1
	
	table_features = u'<features tabularvalignment="' + lyx_table.tabularvalignment + '">\n'
	features_output = u''
	for table_col in lyx_table.columns:
		col_output = u'<column alignment="' + table_col.alignment + '" width="' + \
			word2lyxTableUnits(table_col.width, table_col.units) + '">\n'
		features_output = features_output + col_output
	table_features = table_features + features_output
	
	return table_header + table_features + table_output + table_foot