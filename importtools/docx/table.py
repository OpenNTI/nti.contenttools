from . import _DocxStructureElement
from . import properties as docx

class Table( _DocxStructureElement ):
    grid = []
    borders = []

    @classmethod
    def process( cls, table, doc, rels=None ):
        me = cls()

        if rels is None:
            rels = doc.relationships

	# Parse element and determine table properties
        for element in table.iterchildren():
            if element.tag == '{'+docx.nsprefixes['w']+'}tblGrid':
                process_grid( element, doc, me, rels=rels )
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblPr':
                process_tableproperties( element, doc, me, rels=rels )
            elif element.tag == '{'+docx.nsprefixes['w']+'}tr':
                me.add_child( Table.Row.process(element, doc, rels=rels ) )
            else:
                print('Did not handle table element: %s' % element.tag)

        return me

    class Row( _DocxStructureElement ):

        @classmethod
        def process( cls, row, doc, rels=None ):
            me = cls()

            if rels is None:
                rels = doc.relationships

                for element in row.iterchildren():
                    if element.tag == '{'+docx.nsprefixes['w']+'}tc':
                        me.add_child( Table.Cell.process( element, doc, rels=rels ) )
                    else:
			print('Did not handle table row element: %s' % element.tag)

            return me

        class Cell( _DocxStructureElement ):

            @classmethod
            def process( cls, cell, doc, rels=None ):
                me = cls()

                if rels is None:
                    rels = doc.relationships

                    for element in cell.iterchildren():
                        if element.tag == '{'+docx.nsprefixes['w']+'}p':
                            me.add_child( processParagraph( element, doc, rels=rels ) )
                        else:
                            print('Did not handle table cell element: %s' % element.tag)

                return me


def process_tableproperties( properties, doc, table, rels=None ):
    if rels is None:
        rels = doc.relationships

    for element in properties.iterchildren():
        if element.tag == '{'+docx.nsprefixes['w']+'}tc':
            pass
        else:
            print('Did not handle table property element: %s' % element.tag)

def process_border( border, doc, properties, rels=None ):
    if rels is None:
        rels = doc.relationships

    for element in grid.iterchildren():
        if element.tag == '{'+docx.nsprefixes['w']+'}bottom':
            pass
        elif element.tag == '{'+docx.nsprefixes['w']+'}end':
            pass
        elif element.tag == '{'+docx.nsprefixes['w']+'}insideH':
            pass
        elif element.tag == '{'+docx.nsprefixes['w']+'}insideV':
            pass
        elif element.tag == '{'+docx.nsprefixes['w']+'}start':
            pass
        elif element.tag == '{'+docx.nsprefixes['w']+'}top':
            pass

def process_grid( grid, doc, table, rels=None ):
    if rels is None:
        rels = doc.relationships

    for element in grid.iterchildren():
        if element.tag == '{'+docx.nsprefixes['w']+'}gridCol':
            if '{'+docx.nsprefixes['w']+'}w' in element.attrib.keys():
                table.grid.append(element.attrib['{'+docx.nsprefixes['w']+'}w'])
            else:
                print('Did not handle table grid property: %s' % element.tag)
        else:
            print('Did not handle table grid element: %s' % element.tag)

    print( table.grid )

def tableProperties(property_list, lyx_table):
	'''Parse the general table properties, such as determining the location of table 
		borders, whether there is a grid in use, and the width of the table.'''

	# Scan the tblProperty elements
	for prop in property_list.iter():

		# Look for general table style settings
		if prop.tag == '{'+docx.nsprefixes['w']+'}tblStyle':
			if '{'+docx.nsprefixes['w']+'}val' in prop.attrib.keys():
				# Apply a grid to the table, activate all borders
				if prop.attrib['{'+docx.nsprefixes['w']+'}val'] == 'TableGrid':
					for border in lyx_table.borders.data.keys():
						lyx_table.borders.data[border] = 'true'

		# Look for table border settings
		if prop.tag == '{'+docx.nsprefixes['w']+'}tblBorders':

			# Apply settings to the border settings for the lyxTable object
			for border in prop.iterchildren():

				# Top Border
				if border.tag == '{'+docx.nsprefixes['w']+'}top':
					lyx_table.borders.data['top'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

				# Bottom Border
				if border.tag == '{'+docx.nsprefixes['w']+'}bottom':
					lyx_table.borders.data['bottom'] = border.attrib['{'+docx.nsprefixes['w']+'}val']	
				# Left Border
				if border.tag == '{'+docx.nsprefixes['w']+'}left':
					lyx_table.borders.data['left'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

				# Right Border
				if border.tag == '{'+docx.nsprefixes['w']+'}right':
					lyx_table.borders.data['right'] = border.attrib['{'+docx.nsprefixes['w']+'}val']
				
				# Inside Horizontal Borders
				if border.tag == '{'+docx.nsprefixes['w']+'}insideH':
					lyx_table.borders.data['insideH'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

				# Inside Veritcal Border
				if border.tag == '{'+docx.nsprefixes['w']+'}insideV':
					lyx_table.borders.data['insideV'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

		# Table Width and Units
		if prop.tag == '{'+docx.nsprefixes['w']+'}tblW':
			lyx_table.width = prop.attrib['{'+docx.nsprefixes['w']+'}w']
			lyx_table.units = prop.attrib['{'+docx.nsprefixes['w']+'}type']

	return lyx_table
	

def tableGridProperties(table_grid, lyx_table):
	'''Parse grid column properties. Looks at the table column properties to set width and text styles. Takes both the element to be parsed and a lyxTable object as input. Returns the lyxTable with column objects appended.'''
	
	# Scan the tblGrid Element for gridCol elements, retrieve relative width for each
	for table_col in table_grid.iter():
		if table_col.tag == '{'+docx.nsprefixes['w']+'}gridCol':
			lyx_col = lyxTableCol()
			lyx_col.width = table_col.attrib['{'+docx.nsprefixes['w']+'}w']
			lyx_table.columns.append(lyx_col)
	
	# Calculate the total number of columns and add to table properties
	lyx_table.numColumns = len(lyx_table.columns)
	return lyx_table
	

def processTableRow(table_row):
	'''Parse table rows. Create table cells, populate with cell properties.'''
	
	# Create table row structure
	lyx_row = lyxTableRow()
	
	# Iterate through the structures for each row, parse properties, locate cells
	for row_sub in table_row.iter():
		
		# Iterate over table cell, find data and properties
		if row_sub.tag == '{'+docx.nsprefixes['w']+'}tc':
			
			# Create table cell, find properties and data
			lyx_cell = lyxTableCell()
			for cell_prop in row_sub.iter():
				
				# Find cell properties, Add to table cell
				if cell_prop.tag == '{'+docx.nsprefixes['w']+'}tcPr':
					for cell_aspect in cell_prop.iter():

						# Cell Width
						if cell_aspect.tag == '{'+docx.nsprefixes['w']+'}tcW':
							lyx_cell.width = cell_aspect.attrib['{'+docx.nsprefixes['w']+'}w']
							lyx_cell.units = cell_aspect.attrib['{'+docx.nsprefixes['w']+'}type']

						# Mutli-column Cells
						if cell_aspect.tag == '{'+docx.nsprefixes['w']+'}gridSpan':
							lyx_cell.span_multicol = 'true'
							lyx_cell.multicol = cell_aspect.attrib['{'+docx.nsprefixes['w']+'}val']

						# Multi-row cells
						if cell_aspect.tag == '{'+docx.nsprefixes['w']+'}vMerge':
							lyx_cell.span_multirow = 'true'
							try:
								lyx_cell.multirow_start = cell_aspect.attrib['{'+docx.nsprefixes['w']+'}val']
							except:
								pass
				
				# Add cell data, translated to a valid LyX structure
				if cell_prop.tag == '{'+docx.nsprefixes['w']+'}p':
					lyx_cell.data = processParagraph(cell_prop, True)
					
					# Parse paragraph properties for text alignment
					for cell_aspect in cell_prop.iter():
						if cell_aspect.tag == '{'+docx.nsprefixes['w']+'}jc':
							lyx_cell.textalign = cell_aspect.attrib['{'+docx.nsprefixes['w']+'}val']

				# Determine cell borders
				if cell_prop.tag == '{'+docx.nsprefixes['w']+'}tcBorders':
					# Iterate through the cell borders and set lyxCell.borders.data
					for border in cell_prop:

						# Top Border
						if border.tag == '{'+docx.nsprefixes['w']+'}top':
							lyx_cell.borders.data['top'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

						# Bottom Border
						if border.tag == '{'+docx.nsprefixes['w']+'}bottom':
							lyx_cell.borders.data['bottom'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

						# Left Border
						if border.tag == '{'+docx.nsprefixes['w']+'}left':
							lyx_cell.borders.data['left'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

						# Right Border
						if border.tag == '{'+docx.nsprefixes['w']+'}right':
							lyx_cell.borders.data['right'] = border.attrib['{'+docx.nsprefixes['w']+'}val']

			# Add the cell to the row
			lyx_row.tableCells.append(lyx_cell)
						
	return lyx_row


