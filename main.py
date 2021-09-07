import os
import revText
import createReport
# https://www.arothuis.nl/posts/one-off-docker-images/
# Create output and input volume. 
# Put also the main 

# docker run -v $pwd/output:/output -v $pwd/input:/input example3
# docker run -b C:/Users/Lionel/Python/dockerPractice/output:output C:/Users/Lionel/Python/dockerPractice/input:input example4
currentDir = os.path.dirname(__file__)


inputPath = f"{currentDir}/input/input.json"

outputPath = f"{currentDir}/output/output.txt"
outputPathpdf = f"{currentDir}/output/output.pdf"


revText.reverseText(inputPath, outputPath)
createReport.createSenseIDReportPDF(inputPath, outputPathpdf)
