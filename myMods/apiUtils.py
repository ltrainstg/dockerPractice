import requests
import keyring
import json
from requests.auth import HTTPBasicAuth
import requests
from requests.structures import CaseInsensitiveDict
    
def getAPIDat(api_url, user, password):
    #password = keyring.get_password('doctorevidence', user )
    try: 
        response = requests.get(api_url,
                                auth = HTTPBasicAuth(user, password),
                                timeout=10)
        return response.json()
    except: 
        #print(api_url + 'took to long. Returning null.') 
        return None


def dfAPItoDict(df, user, password):
    data_temp = """
    {{  
       "skip-classification": true,  
       {}
        "timeout-ms": 180000,  
        "response/filter": {{  
            "responses": {{  
                "document/nodes": {{  
                    "annotations": {{  
                        "subject-id": false,  
                        "selection": false,  
                        "sense": true,  
                        "tags": false  
                    }}  
                }},  
                "id": true,  
                "article/meta": false,  
                "subjects": {{  
                    "filter/default": {{  
                        "paths": {{  
                            "sense": true,  
                            "uri": true  
                        }} 
                    }}  
                }}  
            }}  
        }}  
     }}
    """ 
    
    query_temp = \
    '''
         {{  
           "document/nodes": [  
             {{  
               "node/text": "{}",  
               "mode/unbound-mode?": true  
             }}  
           ],  
           "id": "{}"  
         }}
    '''
    
    q_str_list = list()
    
    # Loop over DF and create the queries 
    for row in df.itertuples():
        query_new = query_temp.format(row[2],row[1])
        q_str_list.append(query_new)        
    q_str = ',\n'.join(q_str_list)
    
    query_str = '''
    "queries": [  
    {}
        ],  
    '''.format(q_str)
    
    data = data_temp.format(query_str)

    url = "https://search.doctorevidence.com/api/annotator/batch-annotate"

    headers = CaseInsensitiveDict()
    #BToken = keyring.get_password("DocSearch", user)
    BToken = password
    headers["Authorization"] = "Bearer " + BToken
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"

    #data = json.dumps(payload)


    resp = requests.post(url, headers=headers, data=data.encode('utf-8'))
    #return(resp)
    newDict = dict()
    
    for a in resp.json()['responses']:
        expectedKeys = list(a['subjects'].keys())
        newDict[a['id']] = a
        if len(expectedKeys) == 1:
            key = list(a['subjects'].keys())[0]
        else:
            #print('Expected Keys should be 1: '+ a['id'])
            key = None
            #break
    
    return(newDict)





