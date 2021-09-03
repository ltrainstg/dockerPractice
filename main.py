import os
# https://www.arothuis.nl/posts/one-off-docker-images/
# Create output and input volume. 
# Put also the main 

# docker run -v $pwd/output:/output -v $pwd/input:/input example3

currentDir = os.path.dirname(__file__)


inputPath = f"{currentDir}/input/input.json"

outputPath = f"{currentDir}/output/output.txt"
outputPathpdf = f"{currentDir}/output/output.pdf"


with open(outputPath, "w") as outputFile:
    with open(inputPath) as inputFile:
        content = inputFile.read()
        outputFile.write(content[::-1])
        

        
from fpdf import FPDF
WIDTH = 210
HEIGHT = 297
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(40, 10, 'HELLO WORLD')
#pdf.image("")
pdf.output(outputPathpdf, 'F')