import os
from fpdf import FPDF
title = 'DRE Report 1'

def test():
    print('test')
    
def addFullPageLandscapeImage(pdf, txt, outfile, w = 250, x = 0, y =75):
    pdf.add_page(format = (350,300))
    pdf.multi_cell(0, 5, txt, ln = True, align='C')
    #w = 250
    h = w*2/3
    pdf.image(outfile, w = w, h = h,x=x, y=y)
    pdf.add_page()
    
def convertDF(df, newCol):    
    N = list(df.columns.values)
    N.insert(0, newCol)
    df[newCol] =  df.index
    df = df[N]
    return(df)

def addDFtoPDF(pdf, df, title): 
    data = df.values.tolist()
    data.insert(0, df.columns.to_list())
    pdf.create_table(table_data = data,title=title, cell_width='uneven')
    
def pasteME(x):
    x = [a for a in x if pd.isnull(a) == False]
    return '|'.join(x)

    
class DREPDF(FPDF):
    title = 'title'
    website = 'www.google.com'
    imagePath = 'ect/DRE.png'
    max_width = '400'
    
    def set_website(self, web):
        self.website = web
    def set_imagePath(self, imagePath):
        self.imagePath = imagePath
    def set_maxWidth(self, max_width):
        self.max_width = max_width
        
    def header(self):
        self.image(self.imagePath, 10, 8, 25)
        
        # font
        self.set_font('helvetica', 'B', 15)
        # Calculate width of title and position
        title_w = self.get_string_width(self.title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        # colors of frame, background, and text
        self.set_draw_color(255,255, 255) # border = blue
        self.set_fill_color(44, 58, 81) # background = yellow
        self.set_text_color(255, 255, 255) # text = red
        # Thickness of frame (border)
        self.set_line_width(1)
        # Title
        self.cell(title_w, 10, self.title, border=1, ln=1, align='C', fill=1, link = self.website)
        # Line break
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 12)
        self.cell(0, 10, f'Page{self.page_no()}/{{nb}}', align = 'C')

        
        
    def render_table_header(self, TABLE_COL_NAMES, col_width):
        line_height = self.font_size * 2.5
        
        if isinstance(col_width, list):
            col_width = col_width.reverse()

                
        self.set_fill_color(8, 38, 88) # background = yellow
        self.set_text_color(120, 120, 120) # text = red

        for col_name in TABLE_COL_NAMES:
            if isinstance(col_width, list):
                cw = col_width.pop()
            else:
                cw = col_width
                self.cell(cw, line_height, col_name, border=1, fill = True)
        self.set_fill_color(0, 0, 0) # white
        self.set_text_color(0, 0, 0) # white    
        self.ln(line_height)




    def create_table(self,
                     table_data,
                     title='', 
                     data_size = 10,
                     title_size=12,
                     align_data='L',
                     align_header='L',
                     cell_width='even',
                     x_start='x_default',
                     emphasize_data=[], 
                     emphasize_style=None,
                     emphasize_color=(0,0,0)): 
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: 
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """
        # Convert table data to strings
        table_data = [[str(j) for j in i] for i in table_data]
        
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
           
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                total_width = sum(col_widths)
                
                if total_width > self.max_width:
                    # print(col_widths)
                    col_widths = [i/total_width*self.max_width for i in col_widths]                
                col_width = col_widths
                
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font('helvetica', '', 12)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height) # move cursor back to the left margin

        self.set_font('helvetica', '', data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            self.render_table_header(header, col_width)

            for row in data:
                if self.will_page_break(line_height):
                    self.render_table_header(header, col_width)
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    datum = str(datum)
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font('helvetica', '', emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font('helvetica', '', default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font('helvetica', '', emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font('helvetica', '', default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left,y3,x_right,y3)
        

