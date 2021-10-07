from IPython.display import *
import ipywidgets as widgets
from ipywidgets import *
from utils import *
import pandas as pd 

def getBox(l = None):
    if l is None:
        l = Layout(flex='0 1 auto', height='300px', min_height='40px', width='auto')
    b1 = widgets.Textarea(
    value='',
    placeholder='Type something',
    description='String:',
    disabled=False, 
    layout=l
    )
    return (b1)


def twoDFComp(api1_df, api2_df):
    a = widgets.Text()
    def f1(a):
        c = api1_df.query("Name == @a")
        display(c)
    def f2(a):
        c = api2_df.query("Name == @a")
        display(c)
    out1 = widgets.interactive_output(f1, {'a': a})
    out2 = widgets.interactive_output(f2, {'a': a})
    
    display(a)
    display(out1)
    display(out2)

def getApiBrowser(api_storage_dict1, api_storage_dict2):
    
    x_widget = Dropdown(options = list(api_storage_dict1.keys()))

    y_opt = list(api_storage_dict1[list(api_storage_dict1.keys())[0]].keys())
    y_opt.sort()
    y_widget = Dropdown(options = y_opt)
    # Define a function that updates the content of y based on what we select for x
    b1 = getBox()
    b2 = getBox()

    toggle = widgets.ToggleButton(
        value=False,
        description='Click me',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Description',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )



    def update(*args):
        o = list(api_storage_dict1[x_widget.value].keys())
        o.sort()
        y_widget.options = o

    def update1(*args):
        if y_widget.value != None: 
            b1.value = str(api_storage_dict1[x_widget.value][y_widget.value])
        else:
            b1.value = "NA"

    def update2(*args):
        if y_widget.value != None: 
            b2.value = str(api_storage_dict2[x_widget.value][y_widget.value])
        else:
            b2.value = "NA"

    x_widget.observe(update)   
    toggle.observe(update1)
    toggle.observe(update2)

    return(widgets.VBox([x_widget, y_widget, toggle, b1, b2]))

def getVennFile(api1_df, api2_df):
    x_widget = Dropdown(options = list(api_storage_dict1.keys()))
    # Define a function that updates the content of y based on what we select for x

    l = Layout(flex='0 1 auto', height='400px', min_height='400px', width='400px')

    b1 = getBox(l)
    b2 = getBox(l)
    b3 = getBox(l)


    toggle = widgets.ToggleButton(
        value=False,
        description='Click me',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Description',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )

    def getInCommon(file):
        lst1 = api1_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        lst2 = api2_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        incommon = intersection(lst1, lst2)
        return(incommon)

    def getLeft(file):
        incommon = getInCommon(file)
        lst2 = api2_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        incommon = Diff(lst2, incommon)
        return(incommon)

    def getRight(file):
        incommon = getInCommon(file)
        lst1 = api1_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        incommon = Diff(lst1, incommon)
        return(incommon)

    def update(*args):
        y_widget.options = list(api_storage_dict1[x_widget.value].keys())

    def update1(*args):
        b1.value  = str(getRight(x_widget.value))
        #print(b1.value)

    def update2(*args):
        b2.value  = str(getInCommon(x_widget.value))

    def update3(*args):
        b3.value  = str(getLeft(x_widget.value))
        #Diff(lst1, incommon)

    x_widget.observe(update)   
    #x_widget.observe(update1)
    #y_widget.observe(update1)
    #x_widget.observe(update2)
    #y_widget.observe(update2)


    toggle.observe(update1)
    toggle.observe(update2)
    toggle.observe(update3)
    A = HBox([b1, b2, b3])

    return(widgets.VBox([x_widget, toggle, A]))



def VennView(api1_df, api2_df):
    x_widget = widgets.Dropdown(options = list(set(api1_df.File)))
    # Define a function that updates the content of y based on what we select for x
    l = Layout(flex='0 1 auto', height='400px', min_height='400px', width='400px')
    b1 = getBox(l)
    b2 = getBox(l)
    b3 = getBox(l)
    toggle = widgets.ToggleButton(
        value=False,
        description='Click me',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Description',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    def update1(*args):
        b1.value  = x_widget.value
        #print(b1.value)

    def update1(*args):
        b1.value  = str(getSide(x_widget.value, api1_df, api2_df, 'left'))
        #print(b1.value)

    def update2(*args):
        b2.value  = str(getInCommon(x_widget.value, api1_df, api2_df))

    def update3(*args):
        b3.value  = str(getSide(x_widget.value, api1_df, api2_df, 'right'))
        #Diff(lst1, incommon)

    toggle.observe(update1)
    toggle.observe(update2)
    toggle.observe(update3)
    A = HBox([b1, b2, b3])

    return(widgets.VBox([x_widget, toggle, A]))

def seeSingleDiff(api1_df, api2_df):
    a = widgets.Dropdown(
    options=list(set(api1_df.File)),
    description='Number:',
    disabled=False,
    )
    def f1(a):
        file = a
        incommon = getInCommon(file, api1_df, api2_df)
        left = api1_df.query("File == @file").query("Name in @incommon")
        left.rename(columns={"Sense_ID":"Sense_ID_L"})
        right = api2_df.query("File == @file").query("Name in @incommon")
        c = pd.merge(left, right, on=["File", "Name", "N_IDS"]).query("Sense_ID_x != Sense_ID_y")
        display(c)       


    
    out1 = widgets.interactive_output(f1, {'a': a})
    display(a)
    display(out1)