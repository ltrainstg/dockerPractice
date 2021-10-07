# Fix1 is if one api gives a single return and the other gives multiple 
# If the single is in the multi assign the single 
# Return new API1.df
import utils
import pandas as pd
from tqdm import tqdm   




def applyFix1(multi_df1, single_df2):
    audit_dict = dict()
    for file in single_df2.File.unique():
        print(file)
        lst = utils.getSide(file, single_df2, multi_df1, direction = 'left')
        lst = tqdm(lst, total=len(lst), desc="Parsing Terms in" + file)        
        for item in lst: 
            #print(item)
            if not any(multi_df1['Name']==item):
                continue
            if not any(single_df2['Name']==item):
                continue
            multi_i = multi_df1.index[(multi_df1['Name']==item) & (multi_df1['File']==file) ].tolist()[0]
            single_i = single_df2.index[(single_df2['Name']==item) & (single_df2['File']==file) ].tolist()[0]
            multi = multi_df1.at[multi_i, 'Sense_ID']
            single = single_df2.at[single_i, 'Sense_ID'][0]
            if single in multi:
                audit_dict[item] = {'single': single, 'multi': multi,  'newMulti': single_df2.at[single_i, 'Sense_ID']}
                multi_df1.at[multi_i, 'Sense_ID'] = [single]
                multi_df1.at[multi_i, 'N_IDS'] = 1
                #break
    return_l = [multi_df1, audit_dict]
    return(return_l)

# Fix2 is if one api gives a single return and the other gives multiple 
# If the single has a parent term in the multiple
# If it's only one match switch to that since we assume the single items is a specific case of a subset of the parent term in multi. 
# If it's multiple report the single item since it's a probably a composite of the multi senseID items. 
# Return new multi 


def applyFix2(single_df, multi_df):
    user = 'lduarte@doctorevidence.com'
    audit_dict = dict()
    for file in single_df.File.unique():
        print(file)
        lst = utils.getSide(file, single_df, multi_df, direction = 'left')
        lst = tqdm(lst, total=len(lst), desc="Parsing Terms in" + file)
        for item in lst: 
            #print(item)
            if not any(single_df['Name']==item):
                continue
            if not any(multi_df['Name']==item):
                continue
            single_i = single_df.index[(single_df['Name']==item) & (single_df['File']==file) ].tolist()[0]
            multi_i = multi_df.index[(multi_df['Name']==item) & (multi_df['File']==file) ].tolist()[0]
            single = single_df.at[single_i, 'Sense_ID'][0]
            multi = multi_df.at[multi_i, 'Sense_ID']
            api_url = 'https://caladan.doctorevidence.com/portal/Term/' + single
            single_data = apiUtils.getAPIDat(api_url, user)
            if single_data is None:
                continue
            # Check if the Sense.ID returns a label that matches the item then it is the match
            labelMatch = item.lower() in [a.lower() for a in single_data['labels']] 
            if labelMatch:
                audit_dict[item] = {'single': single, 'multi': multi, 'parentTerms': single_data['parentTerms'], 'newMatch': single, 'type': 'Match'}
                multi_df.at[multi_i, 'Sense_ID'] = [single]
                multi_df.at[multi_i, 'N_IDS'] = 1
                continue

            intersect = intersection(single_data['parentTerms'], multi)
            if len(intersect) == 0:
                continue
            # If single has a parent term that matches the multi. 
            # Then assume it's a subset. 
            if len(intersect) == 1:
                audit_dict[item] = {'single': single, 'multi': multi, 'parentTerms': single_data['parentTerms'], 'newMatch':  [intersect[0]],  'type': 'Assume single is subset of multi'}
                multi_df.at[multi_i, 'Sense_ID'] = [intersect[0]]
                multi_df.at[multi_i, 'N_IDS'] = 1
                continue 
            if len(intersect) >= 1:
                audit_dict[item] = {'single': single, 'multi': multi, 'parentTerms': single_data['parentTerms'], 'newMatch': [single],  'type': 'Assume single is compound of multi'}
                multi_df.at[multi_i, 'Sense_ID'] = [single]
                multi_df.at[multi_i, 'N_IDS'] = 1
                single_df.at[single_i, 'Sense_ID'] = [single]
                    
    return_l = [multi_df, single_df, audit_dict]
    return(return_l)