# dockerPractice
Practice Using Docker on git

# Main Link
https://www.arothuis.nl/posts/one-off-docker-images/

# Goal 
Given an a custom file framework of Nodes and strings to map for those nodes use a few doc APIs to map the strings to Sense.ID and create several audit files and intermediary files to parse. 
This will be a stand alone application using docker. 

## Inputs 

A dict of dicts called **api_empty_dict.json**. 
E.G. {'Disease': {'type 2 diabetes mellitus', 'sarcoma', 'gout'}}


## Process 
Get the **api_empty_dict.json** and query the two APIs
 * Analytics: https://caladan.doctorevidence.com/portal/suggestions?search={stroke}
 * Search: https://search.doctorevidence.com/api/annotator/batch-annotate

Next the apis are compared to see if they are in agreement. Ideally each string returns only 1 Sense.ID and both APIs return the same one. 
This is not always the case and a series of assumptions are made and documented to get the 2 APIs more inline. 
Finally a report, appendix, and audit file is created. 
 

## Output Schema
The *output* folder cintains 2 pdfs one for the report and one for the appendix tables of audit files. 
The *rawData* contains the filled in **api_empty_dict.json** from the api result.
The *parsedData* folder contains a formated Data.Frame that is used in analysis. 
The *images* folder contains the images inserted into the pdf.



``` 
Output
├──report.pdf
├──Appendix.pdf
├──apiAuditFile.pkl
├── rawData
│   ├── analyticsAPI_dict.pkl
│   ├── searchAPI_dict.pkl
├── parsedData
│   ├── analyticsAPI_DF.pkl
│   ├── searchAPI_DF.pkl
├── images
│   ├── filename*.png

```

## Filetypes 

*.pkl: This is just an internal python data dump file that can be read with the pickle library. 


## Call 

Docker use local folders for inputs and outputs passed as volumes.  
The input folder should contain a file called **api_empty_dict.json**
The output folder should be empty.  

Example call: docker run -v $pwd/output:/output -v $pwd/input:/input example1


# TBD

* The outputs currently expect 9 nodes to create a 3x3.

