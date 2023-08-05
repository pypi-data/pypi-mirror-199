'''
Utils for framework usage

Heitor Gessner,
21/03/2023
'''

def grab_basic_framework():
    '''
    Returns the string version of create_framework_file()
    '''
    basic_text = '''
\'\'\'
Basic framework concept

Created by,
Heitor Gessner
\'\'\'

import os
import json

import numpy as np
import pandas as pd
import aesplot

def linear(x,a,b):
    return a*x+b

data_path = "./data/data.csv" #expect csv type
save_path = './img/example'
fig_name = 'Example'
example = aesplot.PlotLikeR()
example.load_data(f'{data_path}',x='Brain volume mm3', y='Amygdala volume mm3')

example.linear = linear    #This is how you can add a function to be fitted
                        #In this case, the linear function for the linear regression
                        #Is already included. But one might find necessary to add
                        #Other fitting functions.

##Removing species
filter = {
    'data':{'Specie':['Hippopotamus amphibius','Trichecus manatus','Loxodonta africana']}
}
example.filter_sub_data(filter) #the default is to remove

example.apply_to_x(np.log)     #Dont use the parenteses after de the function!!
example.apply_to_y(np.log)     #It has to be np.log10 and not np.log10()
                            #Or in this case np.log, to take the ln of the data

groups = {
    'Order':[
    {'cet':'Cetacea'},              #First comes the name of the group you want to create
    {'sotalia':'Cetacea'},          #Next comes the values that will be included
    {'cet_no_outlier':'Cetacea'},   #Note that this can/will be filtered in the future!!
    {'cet_and_sotalia':'Cetacea'},
    {'chosen_data':['Insectivores', 'Scandentia', 'Primates', 'Carnivores', 'Pinnipeds',
     'Perrisodactyla', 'Xenarthra', 'Megachirpotera', 'Microchiroptera',
     'Afrotheria', 'Pholidota', 'Artiodactyla', 'Perissodactyla']} #Can also include a list
    ]
}
example.select_plot(groups)


##removing outlier from multiple
filter = {
    'cet_no_outlier':{'Specie':['Lagenorhynchus obliquidens']},
    'cet_and_sotalia':{'Specie':['Lagenorhynchus obliquidens']}
}
amyg.filter_sub_data(filter)

#Managing sotalia
filter = {'cet_no_outlier':{'Specie':['Sotalia Guianensis']}}
example.filter_sub_data(filter)
filter = {'sotalia':{'Specie':['Sotalia Guianensis']}}
example.filter_sub_data(filter,remove=False) #instead of revoming, keep only S.G.

params = { #params will be used soon to plot everything

    # cet includes the outlier but doen't include Sotalia
    "cet":{
        'scatter_plot':True, #scatter plot and allows the bellow options
        "cs":"darkcyan", #color of scatter plot
        "ss":5, #size of scatter plot (big or small dots)
        "marker":"o", #marker type, check https://matplotlib.org/stable/api/markers_api.html
        "label":"Cetaceans" #labels the scatter plot data
    },

    #Single point for scatter (single point) plot
    "sotalia":{'scatter_plot':True,
            "cs":"darkcyan",
            "ss":100,
            "marker":"*",
            'label':'' #Empty labels wont be shown!!
    },

    #data without outlier to be fitted in linear regression
    "cet_no_outlier":{
            'plot_linear':True, #the order doesn't matter!
            "cp":"black",
            "lwp":1., #line width for the plot (float)
            'alphap':1., #alpha value for the plot
            "marker":"*",
            "rib":True, #plot the Confidence Interval (ribbon)

            'cci':"silver", #Color of CI -> Note:
                            #there's no alpha value cci due to complications
                            #with matplotlib. Use a lighter color or equivalent
                            #hex value

            'zorder':1,     #Small number to be plotted behind,
                            #or big number to be plotted in front
                            #Not necessary to use, but it's there

            'label':'' #Empty labels wont be shown!!
    },

    #all non-cetaceans mammals
    "chosen_data":{'plot_fit_to':'linear',  #this will plot and fit an especific
                                            #In this example, it is the same as a
                                            #Linear regression (plot_linear) but it
                                            #Could be, for example, an exponencial curve
            "cf":"black", #curve fitted color
            'scatter_plot':True,
            "cs":"black",
            "ss":5,
            "marker":"s",
            "rib":True,
            'cci':"lightgrey",
            "label":"Non-Cetacean Mammals",
            'global': True #Set to True to get the entire interval of the final image
    }
}

##Note that cet_and_sotalia wont be plotted since it is
##not included in the params
example.plot(params)
example.set_yticks(arange=np.arange(2.5,11,2.5))
example.set_yticks(arange=np.arange(1.25,11,1.25),which='minor')
example.set_xticks(arange=np.arange(4,15,4))
example.set_xticks(arange=np.arange(4,15,2),which='minor')

legend = {
    's':60 #size of the marker
}
example.set_legend_marker(legend)

example.save_results()
example.save_plots(path=save_path,file='example.png')
example.show()
'''
    return basic_text

def create_framework_file(path='./',file_name='basic_framework.py'):
    '''
    Generates a python file with a basic concept of usage for
    aesplot as a framework
    '''
    if isinstance(path,str):
        if path and not path[-1]=='/':
            path+='/'
    else:
        print(f'Your path {path} was not a string, setting path to cwd')
        path='./'
    basic_text = '''
\'\'\'
Basic framework concept

Created by,
Heitor Gessner
\'\'\'

import os
import json

import numpy as np
import pandas as pd
import aesplot

def linear(x,a,b):
    return a*x+b

data_path = "./data/data.csv" #expect csv type
save_path = './img/example'
fig_name = 'Example'
example = aesplot.PlotLikeR()
example.load_data(f'{data_path}',x='Brain volume mm3', y='Amygdala volume mm3')

example.linear = linear    #This is how you can add a function to be fitted
                        #In this case, the linear function for the linear regression
                        #Is already included. But one might find necessary to add
                        #Other fitting functions.

##Removing species
filter = {
    'data':{'Specie':['Hippopotamus amphibius','Trichecus manatus','Loxodonta africana']}
}
example.filter_sub_data(filter) #the default is to remove

example.apply_to_x(np.log)     #Dont use the parenteses after de the function!!
example.apply_to_y(np.log)     #It has to be np.log10 and not np.log10()
                            #Or in this case np.log, to take the ln of the data

groups = {
    'Order':[
    {'cet':'Cetacea'},              #First comes the name of the group you want to create
    {'sotalia':'Cetacea'},          #Next comes the values that will be included
    {'cet_no_outlier':'Cetacea'},   #Note that this can/will be filtered in the future!!
    {'cet_and_sotalia':'Cetacea'},
    {'chosen_data':['Insectivores', 'Scandentia', 'Primates', 'Carnivores', 'Pinnipeds',
     'Perrisodactyla', 'Xenarthra', 'Megachirpotera', 'Microchiroptera',
     'Afrotheria', 'Pholidota', 'Artiodactyla', 'Perissodactyla']} #Can also include a list
    ]
}
example.select_plot(groups)


##removing outlier from multiple
filter = {
    'cet_no_outlier':{'Specie':['Lagenorhynchus obliquidens']},
    'cet_and_sotalia':{'Specie':['Lagenorhynchus obliquidens']}
}
amyg.filter_sub_data(filter)

#Managing sotalia
filter = {'cet_no_outlier':{'Specie':['Sotalia Guianensis']}}
example.filter_sub_data(filter)
filter = {'sotalia':{'Specie':['Sotalia Guianensis']}}
example.filter_sub_data(filter,remove=False) #instead of revoming, keep only S.G.

params = { #params will be used soon to plot everything

    # cet includes the outlier but doen't include Sotalia
    "cet":{
        'scatter_plot':True, #scatter plot and allows the bellow options
        "cs":"darkcyan", #color of scatter plot
        "ss":5, #size of scatter plot (big or small dots)
        "marker":"o", #marker type, check https://matplotlib.org/stable/api/markers_api.html
        "label":"Cetaceans" #labels the scatter plot data
    },

    #Single point for scatter (single point) plot
    "sotalia":{'scatter_plot':True,
            "cs":"darkcyan",
            "ss":100,
            "marker":"*",
            'label':'' #Empty labels wont be shown!!
    },

    #data without outlier to be fitted in linear regression
    "cet_no_outlier":{
            'plot_linear':True, #the order doesn't matter!
            "cp":"black",
            "lwp":1., #line width for the plot (float)
            'alphap':1., #alpha value for the plot
            "marker":"*",
            "rib":True, #plot the Confidence Interval (ribbon)

            'cci':"silver", #Color of CI -> Note:
                            #there's no alpha value cci due to complications
                            #with matplotlib. Use a lighter color or equivalent
                            #hex value

            'zorder':1,     #Small number to be plotted behind,
                            #or big number to be plotted in front
                            #Not necessary to use, but it's there

            'label':'' #Empty labels wont be shown!!
    },

    #all non-cetaceans mammals
    "chosen_data":{'plot_fit_to':'linear',  #this will plot and fit an especific
                                            #In this example, it is the same as a
                                            #Linear regression (plot_linear) but it
                                            #Could be, for example, an exponencial curve
            "cf":"black", #curve fitted color
            'scatter_plot':True,
            "cs":"black",
            "ss":5,
            "marker":"s",
            "rib":True,
            'cci':"lightgrey",
            "label":"Non-Cetacean Mammals",
            'global': True #Set to True to get the entire interval of the final image
    }
}

##Note that cet_and_sotalia wont be plotted since it is
##not included in the params
example.plot(params)
example.set_yticks(arange=np.arange(2.5,11,2.5))
example.set_yticks(arange=np.arange(1.25,11,1.25),which='minor')
example.set_xticks(arange=np.arange(4,15,4))
example.set_xticks(arange=np.arange(4,15,2),which='minor')

legend = {
    's':60 #size of the marker
}
example.set_legend_marker(legend)

example.save_results()
example.save_plots(path=save_path,file='example.png')
example.show()
'''
    with open(f'{path}{file_name}','w') as file:
        file.write(basic_text)
