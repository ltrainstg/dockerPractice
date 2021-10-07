from matplotlib_venn import venn2 

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def getInCommon(file, left_df, right_df):
    lst1 = left_df.query("File == @file").query("N_IDS == 1").Name.to_list()
    lst2 = right_df.query("File == @file").query("N_IDS == 1").Name.to_list()
    incommon = intersection(lst1, lst2)
    incommon.sort()
    return(incommon)

def getSide(file, left_df, right_df, direction):
    incommon = getInCommon(file, left_df, right_df)
    if direction == 'left':
        df = left_df
    if direction == 'right':
        df = right_df    
    lst = df.query("File == @file").query("N_IDS == 1").Name.to_list()
    side = Diff(lst, incommon)
    side.sort()
    return(side)

# get Venn


def vennFromLst(lst1, lst2):
    inBoth = len(intersection(lst1, lst2))
    inA = len(lst1) - inBoth
    inB = len(lst2) - inBoth
    # depict venn diagram
    venn2(subsets = (inA, inB, inBoth), set_labels = ('Group A', 'Group B'))
    
def getSingleInMulti(single_df, multi_df, lst):    
    i = 0 
    for item in lst:
        #print(item)
        if item not in single_df.Name.tolist():
            continue
        if item not in multi_df.Name.tolist():
            continue
        single = single_df.query("Name == @item").iloc[0]['Sense_ID']
        if len(single) == 0:
            continue
        multi = multi_df.query("Name == @item").iloc[0]['Sense_ID']
        if single[0] in multi:
            i = i+1
    return(i)