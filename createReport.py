from fpdf import FPDF
def createSenseIDReportPDF(inputPath, outputPath):
    WIDTH = 210
    HEIGHT = 297
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(40, 10, 'HELLO WORLD')
    #pdf.image("")
    pdf.output(outputPath, 'F')