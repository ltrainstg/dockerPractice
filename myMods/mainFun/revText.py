def reverseText(inputPath, outputPath):
    with open(outputPath, "w") as outputFile:
        with open(inputPath) as inputFile:
            content = inputFile.read()
            outputFile.write(content[::-1])