import pickle 
import pandas as pd
import math
import numpy as np
from tqdm import tqdm
import apiUtils



def parseAnalyticsAPI(api_storage_dict):  
    rows = []
    for key1 in api_storage_dict:
        for key2 in api_storage_dict[key1]:
            ids = []
            if api_storage_dict[key1][key2] is None:
                rows.append([key1, key2, 0, ids])
                continue
            for a in api_storage_dict[key1][key2]:
                ids.append(a['id'])
            ids = list(set(ids))
            rows.append([key1, key2, len(ids), ids])
    analytics_df = pd.DataFrame(rows)
    analytics_df.columns = ['File','Name','N_IDS','Sense_ID']
    return(analytics_df)

def parseSearchAPI(api_storage_dict):
    rows = []
    for key1 in api_storage_dict:
        for key2 in api_storage_dict[key1]:
            ids = set()
            for key in api_storage_dict[key1][key2]['subjects']:
                if 'sense' not in api_storage_dict[key1][key2]['subjects'][key]['paths'][0][0]:
                    continue
                for b in api_storage_dict[key1][key2]['subjects'][key]['paths']:
                    ids = ids.union(set(pd.DataFrame(b).sense))
            ids = list(ids)
            rows.append([key1, key2, len(ids), ids])
    search_df = pd.DataFrame(rows)
    search_df.columns = ['File','Name','N_IDS','Sense_ID']  
    return(search_df)



def analyticsAPI(api_empty_dict, user, server, password):
    api_url_fmt = "https://{}.doctorevidence.com/portal/suggestions?search={}"
    for nodeFile in api_empty_dict:
        term_queue = tqdm(api_empty_dict[nodeFile].keys(), total=len(api_empty_dict[nodeFile]), desc="Parsing Terms in" + nodeFile)    
        for name in term_queue:
            api_url = api_url_fmt.format(server, name)
            json_data = apiUtils.getAPIDat(api_url, user, password)
            api_empty_dict[nodeFile][name] = json_data
    return(api_empty_dict)



def searchAPI(api_empty_dict, user, server, df_size, password):
    for nodeFile in api_empty_dict:
        df = pd.DataFrame([api_empty_dict[nodeFile].keys(), api_empty_dict[nodeFile].keys()]).T
        df.columns = ['name', 'name']
        n_group = max(1, math.floor(len(df)/df_size))
        split_df_list =np.array_split(df, n_group)
        term_queue = tqdm(split_df_list, total=len(split_df_list), desc="Parsing Terms in "+nodeFile)   
        for split_df in term_queue: 
            api_empty_dict[nodeFile].update(apiUtils.dfAPItoDict(split_df, user,password))
    return(api_empty_dict)
            
            
            
            
            
            
def loadPickle(p_file):
    data  = pickle.load( open(p_file , "rb" ) )
    return data












def loadAPI1DF(p_file):
    api_storage_dict1  = loadPickle(p_file)
    senseList = []
    for fileKey in api_storage_dict1.keys():
        for key in api_storage_dict1[fileKey].keys():
            d = api_storage_dict1[fileKey][key][0]
            df = pd.DataFrame(d)
            if 'id' in df.columns.tolist():
                ids = df.id.unique().tolist()
            else:
                ids = []
            senseList.append([fileKey, key, len(ids), ids])
    df = pd.DataFrame(senseList, columns = ['File','Name', 'N_IDS', 'Sense_ID'])
    return df

def loadAPI2DF(p_file):
    api_storage_dict2  = loadPickle(p_file)
    senseList = []
    for file in api_storage_dict2.keys():
        for name in api_storage_dict2[file].keys():     
            a = api_storage_dict2[file][name]['subjects']
            s = list()
            for key in a.keys():
                b = a[key]
                for i in range(0,len(b['paths'])):
                    df = pd.DataFrame(b['paths'][i])
                    if 'sense' in df.columns.to_list():
                        slist =pd.DataFrame(b['paths'][i]).sense.to_list()
                s.extend(slist)
                senseList.append([file, name, len(s), s])
    df = pd.DataFrame(senseList, columns = ['File','Name', 'N_IDS', 'Sense_ID'])
    return df
                

                