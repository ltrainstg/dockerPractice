# https://www.arothuis.nl/posts/one-off-docker-images/
# Create output and input volume. 
# Put also the main 

# docker run -v $pwd/output:/output -v $pwd/input:/input example3
# docker run -b C:/Users/Lionel/Python/dockerPractice/output:output C:/Users/Lionel/Python/dockerPractice/input:input example4


# docker run -it --gpus=all --name <name> -v <algo folder>:/algo -v <data folder>:/data --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" tensorflow/tensorflow:1.15.2-gpu-py3 /bin/bash

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import json 
import keyring

myMods = os.path.join(os.getcwd(), "myMods")
sys.path.insert(0,myMods)
import mainFun.createReport as createReport
import mainFun.apiFix as apiFix
#import mainFun.getView as getView
import mainFun.loadHelper as loadHelper
import mainFun.vennPlot as vennPlot

# Debug info 
print(sys.executable)
print(sys.version)
currentDir = os.getcwd()




# Mid Files
dirs = ['rawData', 'parsedData', 'images']
for adir in dirs:
    thisDir = "{}/output/{}/".format(currentDir, adir)
    if not os.path.exists(thisDir):
        os.makedirs(thisDir)

analyticsAPI_dict_file = f"{currentDir}/output/rawData/analyticsAPI_dict.pkl"
searchAPI_dict_file = f"{currentDir}/output/rawData/searchAPI_dict.pkl"
analyticsAPI_DF_file = f"{currentDir}/output/parsedData/analyticsAPI_DF.pkl"
searchAPI_DF_file = f"{currentDir}/output/parsedData/searchAPI_DF.pkl"

# output 
report_file = f"{currentDir}/output/report.pdf"
appendix_file = f"{currentDir}/output/appendix.pdf"
audit_file = f"{currentDir}/output/apiAuditFile.pkl"

# Inputs 
empty_dict_file = f"{currentDir}/input/api_empty_dict.json"
process_file = f"{currentDir}/input/process.json"

# Process File

# Get the server we want to query for the apis 
# Get the user and password for docanalytics
# Get the bearer token for DocSearch
# Use keyring to set the password and we use that. 

print('Opening Process File for access info')
with open(process_file, 'r') as openfile:
    process_data = json.load(openfile)    
server = process_data['server']
user = process_data['user']
df_size = process_data['df_size']
#keyring.set_password('doctorevidence', user, process_data['doctorevidence'] )
#keyring.set_password('DocSearch', user, process_data['DocSearch'] )


with open(empty_dict_file, 'r') as openfile:
    api_empty = json.load(openfile)    


# Get Analytics dict from pkl file if it exists. 
print('Accessing API data. Will use mid files if in output folder.')

if os.path.isfile(analyticsAPI_dict_file):
    analyticsAPI_dict  = loadHelper.loadPickle(analyticsAPI_dict_file)
else:
    analyticsAPI_dict = loadHelper.analyticsAPI(api_empty,  user, server, process_data['doctorevidence'] )
    with open(analyticsAPI_dict_file, 'wb') as file:  
        pickle.dump(analyticsAPI_dict, file)    
    

api_df1 = loadHelper.parseAnalyticsAPI(analyticsAPI_dict)

with open(analyticsAPI_DF_file, 'wb') as file:  
    pickle.dump(api_df1, file)
    
    
if os.path.isfile(searchAPI_dict_file):
    searchAPI_dict  = loadHelper.loadPickle(searchAPI_dict_file)
else:     
    searchAPI_dict = loadHelper.searchAPI(api_empty,  user, server, df_size, process_data['DocSearch'])
    with open(searchAPI_dict_file, 'wb') as file:  
        pickle.dump(searchAPI_dict, file)    
        
    
api_df2 = loadHelper.parseSearchAPI(searchAPI_dict)
with open(searchAPI_DF_file, 'wb') as file:  
    pickle.dump(api_df2, file)



print('Starting Report')

plt.rcParams["figure.figsize"] = (20,10)
fig, ax = plt.subplots() 


helpersPath = f"{currentDir}/ect/"
fontPath = f"{currentDir}\ect\DejaVuSansCondensed.ttf"
outputPathpdf = f"{currentDir}/output/output.pdf"

# Create Report 
title = 'DRE Report 1'
website = 'https://www.drevidence.com/'
imagePath = f"{currentDir}/ect/DRE.png"


fixDict = {}


# Create a PDF object
pdf = createReport.DREPDF('P', 'mm', 'Letter')
#pdf = createReport.DREPDF(format="A5")
pdf.set_auto_page_break(auto = True, margin = 15)
pdf.set_font('helvetica', '', 12)
#pdf.add_font('DejaVu', '', fontPath, uni=True)
#pdf.set_font('DejaVu', '', 14)

# metadata
pdf.set_title(title)
pdf.set_author('DRE')
pdf.set_website(website)
pdf.set_imagePath(imagePath)
pdf.add_page()
pdf.set_maxWidth(350)
txt = """
Problem: How do we match an existing ontology to Sense.IDs use in DocAnalytics?

Solution: Using two existing APIs that match strings to Sense.IDs. 
I will assume if both return a single identical Sense.ID then this is a good match.
If they do not match other ad-hoc fixes can be applied and documented in this report. 


Input: A dictionary of dictionaries with the outer dictionary being the desired nodes and inner being the strings in that node to match. 
    E.G. {'Disease': {'type 2 diabetes mellitus', 'sarcoma', 'gout'}}

Output: 
    1. A dictionary of those terms filled out for each API. 
    2. An audit dictionary with the fixes applied
    3. Basic Venn diagrams and other diagnostic images. 
    4. Dataframes of the basic data used in the report. 
    
API1: DocAnalytics
    * This api is how docanalytics identifies terms. 
    * E.G. https://caladan.doctorevidence.com/portal/suggestions?search={stroke}
API2: DocSearch
    * This api is how docsearch identifies terms.
    * E.G. https://search.doctorevidence.com/api/annotator/batch-annotate
"""
pdf.multi_cell(0, 5, txt)
pdf.add_page()








set2 = set()
for row in api_df2.itertuples():
    t1 = (row.File, row.Name)
    set2.add(t1)

set1 = set()
for row in api_df1.itertuples():
    t1 = (row.File, row.Name)
    set1.add(t1)
    
if len(set1 - set2) == 0:
    API1_txt = "API1 includes no addtional terms not from API2"

if len(set1 - set2) != 0:
    API1_txt = "API1 returns {} more terms than API2".format(len(set1 - set2))
    
    
if len(set2 - set1) == 0:
    API2_txt = "API2 includes no addtional terms not from API1"

if len(set2 - set1) != 0:
     API2_txt = "API2 returns {} more terms than API1".format(len(set2 - set1))

        


txt = """
Assumption 1: Do both APIs return for all given strings? 
This is not always the case. A few statements and tables are given below. 

API1: {}
API2: {}
""".format(API1_txt, API2_txt)

pdf.multi_cell(0, 5, txt, ln = True)



if len(set1 - set2) != 0:
    txt = """
    Items matched in API1 but not in API2
    """
    pdf.cell(0, 20, txt, ln = True)
    lst1 = set(api_df1.Name.to_list())
    lst2 = set(api_df2.Name.to_list())
    df = pd.DataFrame(lst1-lst2)
    df.columns = ['Name']
    data = df.values.tolist()
    data.insert(0, df.columns.to_list())
    pdf.create_table(table_data = data,title='API2 terms that did not return data', cell_width='uneven')


if len(set2 - set1) != 0:
    txt = """
    Items matched in API2 but not in API1
    """
    pdf.multi_cell(0, 15, txt, ln = True)
    lst1 = set(api_df1.Name.to_list())
    lst2 = set(api_df2.Name.to_list())
    df = pd.DataFrame(lst2-lst1)
    df.columns = ['Name']
    # df['File'] =  df.index
    data = df.values.tolist()
    data.insert(0, df.columns.to_list())
    pdf.create_table(table_data = data,title='API1 terms that did not return data', cell_width='uneven')

#if not (len(set1 - set2) == 0 & len(set2 - set1)): 
outfile ='output/images/filename.png'
vennPlot.plotVenn1(api_df1, api_df2, filename = outfile) 
txt = """
A Venn Diagram showing the overlap of terms that return at least some data from the API. 
It should be 100% overlap. 

Left: All terms that returned any data for API1. 
Right: All terms that returned any data for API2. 
Intersect: All terms that returned any data for both APIs. 

"""
createReport.addFullPageLandscapeImage(pdf, txt= txt, outfile= outfile, w = 300, x = 25, y = 90)




df = pd.crosstab(index = api_df1['File'], columns = api_df1['N_IDS'])

API1_txt = "API1 returns {}-{} Sense.IDs over {} parsed node string files".format(min(df.T.index),
                                                                       max(df.T.index),
                                                                       len(df.index))

df = pd.crosstab(index = api_df2['File'], columns = api_df2['N_IDS'])
API2_txt = "API2 returns {}-{} Sense.IDs over {} parsed node string files".format(min(df.T.index),
                                                                       max(df.T.index),
                                                                       len(df.index))


txt = """
Assumption 2: Do both APIs return a single Sense.ID for all given strings? 
This is not always the case so a few generated statements and a table for each API with rows as desired nodes are shown below. 

API1: {}
API2: {}
""".format(API1_txt, API2_txt)
pdf.multi_cell(0, 5, txt, ln = True)



txt = """
A frequency table of how many Sense.IDs are retruned per term in each Node for API1
Rows: Desired Nodes
Cols: Number of returned Sense.IDs 
"""
pdf.multi_cell(0, 5, txt, ln = True)
df= pd.crosstab(index = api_df1['File'], columns = api_df1['N_IDS'])
df = createReport.convertDF(df, 'File')
createReport.addDFtoPDF(pdf, df, title = 'API1 Sense.ID frequency table')




txt = """
A frequency table of how many Sense.IDs are retruned per term in each Node for API2
Rows: Desired Nodes
Cols: Number of returned Sense.IDs 
"""

pdf.multi_cell(0, 5, txt, ln = True)
df= pd.crosstab(index = api_df2['File'], columns = api_df2['N_IDS'])
df = createReport.convertDF(df, 'File')
createReport.addDFtoPDF(pdf, df, title = 'API2 Sense.ID frequency table')
pdf.add_page()

# TBD For each node create table 




fig, ax = plt.subplots()    
outfile ='output/images/filename1.png'
vennPlot.VennComparePerfect(api_df1, api_df2, outfile)   
txt = """
Assumption 3: The terms that return a single Sense.ID should be the same. 
This is not always the case as seen by the Venn Diagram. 

Left: All terms that returned a single Sense.ID for API1. 
Right: All terms that returned a single Sense.ID for API2. 
Intersect: All terms that returned a single Sense.ID for both API1 and API2.
Text: A number displaying how many of the intersects are identical. 
"""

createReport.addFullPageLandscapeImage(pdf, txt= txt, outfile= outfile, w = 300, x = 25, y = 90)


fixDict['Mismatch'] ={} 

for file in api_df1.File.unique():
    pdf.add_page()
    #print(file)
    txt = """
    {}: 
    These are the items that are mismatched with only 1 Sense.ID reported. 
    """.format(file)
    
    d1 = api_df1.query('File == @file').query('N_IDS == 1')
    d1 = d1[['Name', 'Sense_ID']]
    d2 = api_df2.query('File == @file').query('N_IDS == 1')
    d2 = d2[['Name', 'Sense_ID']]
    df = pd.merge(d1, d2, on='Name', how='outer').\
        query('Sense_ID_x != Sense_ID_y').\
        dropna()
    
    df.columns =['Name', 'Analytics', 'Search']
    fixDict['Mismatch'][file] = df
    if df.shape[0] == 0:
        stub = "No mismatches found"
    else: 
        stub = "These are the items that are mismatched with only 1 Sense.ID reported."
        
    txt = """
    {}: 
    {}
    """.format(file, stub)
        
    pdf.multi_cell(0, 5, txt, ln = True)
    createReport.addDFtoPDF(pdf, df, title = '')
    





fig, ax = plt.subplots() 
outfile = 'output/images/filename2.png'
vennPlot.checkLeftRigtSubset(api_df1, api_df2, outfile)
txt = """
Assumption 4: If a term returns a single Sense.ID in one API and multiple in the other so long as the single is also in the multiple that is the best match. 

EG. 
API1: ['A']
API2: ['A', 'B']

Assume ['A'] is best match and change API2 to ['A']

This graph looks at all the items that matched 1 single Sense.ID in only one of APIs. 
Then it looks if it is a subset of the term returned by the other API. 
If so we assume the single ID is correct and make the change accordingly. 
"""

createReport.addFullPageLandscapeImage(pdf, txt= txt, outfile= outfile, w = 300, x = 25, y = 90)



# Apply Fix 1 
r = apiFix.applyFix1(api_df1, api_df2)
api1_df = r[0]
fixDict['fix1'] = r[1]

r = apiFix.applyFix1(api_df2, api_df1)
api2_df = r[0]
fixDict['fix2'] = r[1] 


fig, ax = plt.subplots() 
outfile = 'output/images/filename3.png'
vennPlot.VennComparePerfect(api_df1, api_df2, outfile) 
txt = """
A Venn Diagram post 

Left: All terms that returned a single Sense.ID for API1. 
Right: All terms that returned a single Sense.ID for API2. 
Intersect: All terms that returned a single Sense.ID for both API1 and API2.
Text: A number displaying how many of the intersects are identical. 
"""

createReport.addFullPageLandscapeImage(pdf, txt= txt, outfile= outfile, w = 300, x = 25, y = 90)

# fig, ax = plt.subplots() 
# outfile = 'output/images/filename4.png'
# vennPlot.checkLeftRigtSubset(api_df1, api_df2, outfile)
# createReport.addFullPageLandscapeImage(pdf, txt= txt, outfile= outfile, w = 300, x = 25, y = 90)

pdf.output('output/report.pdf', 'F')
print('Ending Report')


print('Starting Appendix')

with open(audit_file, 'wb') as file:      
    pickle.dump(fixDict, file)  
    

#fixDict = loadHelper.loadPickle('fixDict.pkl')
currentDir = os.getcwd()
plt.rcParams["figure.figsize"] = (20,10)
fig, ax = plt.subplots() 

# Extract Data

title = 'DRE Report 1'
website = 'https://www.drevidence.com/'
imagePath = f"{currentDir}/ect/DRE.png"

# Create a PDF object
#pdf = createReport.DREPDF('P', 'mm', 'Letter)
pdf = createReport.DREPDF('P','mm',[375,500])
pdf.set_auto_page_break(auto = True, margin = 15)
pdf.set_font('helvetica', '', 12)
pdf.set_maxWidth(350)
#pdf.add_font('DejaVu', '', fontPath, uni=True)
#pdf.set_font('DejaVu', '', 14)
# metadata
pdf.set_title(title)
pdf.set_author('DRE')
pdf.set_website(website)
pdf.set_imagePath(imagePath)
pdf.add_page()


txt = """

Assumption 4: If a term returns a single Sense.ID in one API and multiple in the other so long as the single is also in the multiple that is the best match. 

The fixes due to assumption 4 are demonstrated below. 
API1 subset of API2: {}
API2 subset of API1: {}
EG. 
    * Name: {}
    * Single: {}
    * Multi: {}
    * newMulti: {}

""".format( len(fixDict['fix1']),
            len(fixDict['fix2']),
            list(fixDict['fix1'].items())[0][0],
            list(fixDict['fix1'].items())[0][1]['single'],
            list(fixDict['fix1'].items())[0][1]['multi'],
            list(fixDict['fix1'].items())[0][1]['newMulti'])

pdf.add_page()
pdf.multi_cell(0, 5, txt)
df = pd.DataFrame(fixDict['fix1']).T
df = createReport.convertDF(df, 'Name')
#df['multi'] = df['multi'].apply(apiUtils.pasteME)
createReport.addDFtoPDF(pdf, df, title = 'Apendix: 1')
pdf.add_page()

df = pd.DataFrame(fixDict['fix2']).T
df = createReport.convertDF(df, 'Name')
#df['multi'] = df['multi'].apply(pasteME)
createReport.addDFtoPDF(pdf, df, title = 'Apendix: 2')
pdf.add_page()


pdf.output('output/Appendix.pdf', 'F')
print('Ending Appendix')
