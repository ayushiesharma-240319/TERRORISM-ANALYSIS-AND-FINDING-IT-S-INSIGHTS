# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 07:11:21 2020

@author: The Ayushie Sharma
"""

import pandas as pd


#!pip install Dash
import dash
import dash_html_components as html
from   dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate

import webbrowser


#this is the place for creating global variables for dash
app = dash.Dash()  #here app is by deafault a global variable and Dash is a class in a dash library

#defining of your function load_data
def load_data():
    
    dataset_name = "global_terror1.csv"
    #df is a local variable
    global df    
    df = pd.read_csv(dataset_name)
    
    month = {
             "January":1,
             "February":2,
             "March":3,
             "April":4,
             "May":5,
             "June":6,
             "July":7,
             "August":8,
             "September":9,
             "October":10,
             "November":11,
             "December":12
        
             }
    
    global month_list
    month_list = [{"label":key,"value":values} for key, values in month.items()]
    
    global date_list
    date_list = [x for x in range (1, 32)]
    
    
    global region_list
    
    region_list = [{'label':str(i), 'value':str(i)} for i in sorted(df['region_txt'].unique().tolist())]
    
    global country_list
    
    country_list = df.groupby('region_txt') ['country_txt'].unique().apply(list).to_dict()
    
    
    global state_list
    
    state_list = df.groupby('country_txt') ['provstate'].unique().apply(list).to_dict()
    
   
    global city_list
    
    city_list =  df.groupby('provstate') ['city'].unique().apply(list).to_dict()
    
    global attack_type_list
    
    attack_type_list = [{'label':str(i), 'value':str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    
   
    global year_list
    year_list = sorted (df['iyear'].unique().tolist())
    
    global year_dict
    year_dict = { str(year) : str(year)  for year in year_list } 
    
    global chart_dropdown_values 
    chart_dropdown_values = { "Terrorist Organisation" : 'gname',
                             "Target Nationality":'natlty1_txt',
                             "Target Type":'targtype1_txt',"Type of Attack":'attacktype1_txt',
                             "Weapon Type":'weaptype!_txt',"Region":'region_txt',"Country Attacked":'country_txt',}

    chart_dropdown_values = [{ 'label': key, 'value': values} for key, values in chart_dropdown_values.items()]

def app_dashboard_ui():
    main_layout = html.Div(style={'backgroundColor':'black', "padding":"5px",'color':'black'}, children =
    [
    html.Br(),
    html.Hr(),
    html.H1(children='...Terrorism Analysis with Insights...',id='Main_title',style = {'textAlign':'center','color':'#ff0080','backgroundColor' :'#00ffbf','padding':'4px'}),
    html.Hr(),
    html.Br(),    
    dcc.Tabs(id = "Tabs", value = "Map", children = [
        
        dcc.Tab(label = "Map tool", id = "Map tool",value = "Map", children = [
            
            dcc.Tabs(id = "subtabs1", value = "WorldMap", children = [ 
                dcc.Tab(label = "World Map tool", id = "World", value = "WorldMap"),
                dcc.Tab(label = "India Map tool", id = "India", value = "IndiaMap")
        
                ]),
            
             html.Div([ 
             dcc.Dropdown(id = 'month',
                          options = month_list,
                          placeholder = 'Select Month',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#bfff00','color':'#ff00ff'},
                          multi = True),
    
             dcc.Dropdown(id = 'date',
                          placeholder = 'Select Date',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#0040ff','color':'#0040ff'},
                          multi = True)
             ],
             style = dict(display = 'flex')
             ),
    
             html.Div([ 
             dcc.Dropdown(id = 'region_dropdown',
                          options = region_list,
                          placeholder = 'Select Region',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#00ffff','color':'#ff00bf'},
                          multi = True),
    
    
             dcc.Dropdown(id = 'country_dropdown',
                          options =[],
                          placeholder = 'Select Country',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#00ff40','color':'#ff4000'},
                          multi = True)
             ],
                  
             style = dict(display = 'flex')
             ),
    
             html.Div([ 
             dcc.Dropdown(id = 'state_dropdown',
                          options = [],
                          placeholder = 'Select State',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#ff8000','color':'#40ff00'},
                          multi = True),
    
    
             dcc.Dropdown(id = 'city_dropdown',#
                          options = city_list,
                          placeholder = 'Select City',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#ff0040','color':'bfff00'},
                          multi = True)
             ],
             
             style = dict(display = 'flex')
             ),
    
    
             dcc.Dropdown(id = 'attack_type_dropdown',
                          options = attack_type_list,
                          placeholder = 'Select Attack-Type',
                          style = {"text-align":'center', "width":'100%','backgroundColor':'#bf00ff','color':'#bfff00'},
                          multi = True),
             
    
             html.Br(),
             html.Br(),
             html.H2(id = 'year_selector', children = "Select the year range..", style = {'text-align':'center',
                                                                                 'color':'#ffff00','backgroundColor':'#8000ff','padding':'4px'}),
             dcc.RangeSlider(
                          id = 'year-slider',
                          min = min(year_list),
                          max = max(year_list),
                          value = [min(year_list),max(year_list)],
                          marks = year_dict ,
                          step = None
                         ),
              html.Br()
                    ]),
            
            
    
              dcc.Tab(label = "Chart tool", id = "Chart tool",value = "chart", children = [
            
                  dcc.Tabs(id = "subtabs2", value = "WorldChart", children = [ 
                       dcc.Tab(label = "World Chart tool", id = "WorldC", value = "WorldChart"),
                       dcc.Tab(label = "India Chart tool", id = "IndiaC", value = "IndiaChart")]),
                           html.Br(),
                           dcc.Dropdown(id = "Chart_Dropdown",
                                options = chart_dropdown_values,
                                placeholder = "Select Option",
                                style = {'text-align':'center','width':'99%'},
                                value = "region_txt"),
                   
                           html.Hr(),
                           html.Br(),
                           dcc.RangeSlider(
                                         id = 'chart_year_slider',
                                         min = min(year_list),
                                         max = max(year_list),
                                         value = [min(year_list),max(year_list)],
                                         marks = year_dict ,
                                         step = None
                                         ),
                           html.Br()
                               
                          ]),
                      ]),
                               
           
             html.Div(id = 'graph-object', children = 'Map will show up here...' , style={'textAlign':'center', 'color':'yellow','font-size':'40%','font-family':'cursive'})
    
              ])
    return main_layout

@app.callback(
    dash.dependencies.Output('graph-object','children'),
   [  
    dash.dependencies.Input('Tabs', 'value'),
    
    dash.dependencies.Input('month','value'),
    
    dash.dependencies.Input('date','value'),
    
    dash.dependencies.Input('region_dropdown','value'),
    
    dash.dependencies.Input('country_dropdown','value'),
    
    dash.dependencies.Input('state_dropdown','value'),
    
    dash.dependencies.Input('city_dropdown','value'),
    
    dash.dependencies.Input('attack_type_dropdown','value'),
    
    dash.dependencies.Input('year-slider','value'),
    
    dash.dependencies.Input('chart_year_slider','value'),
    
    dash.dependencies.Input('Chart_Dropdown','value'),
    
    dash.dependencies.Input('subtabs2','value'),
    
    ]
    )

def update_app_ui(Tabs,month_value,date_value,region_value, country_value, state_value,city_value,attack_type_value, year_value,chart_year_selector,chart_dd_value,subtabs2):
    

    
  if Tabs == "Map":
    
    figure = None
    
    print(type(date_value))
    print(date_value)
    
    print(type(city_value))
    print(month_value)
    
    print(type(date_value))
    print(date_value)
    
    print(type(region_value))
    print(region_value)
    
    print(type(country_value))
    print(year_value)
    
    print(type(state_value))
    print(state_value)
    
    print(type(city_value))
    print(city_value)
    
    print(type(attack_type_value))
    print(attack_type_value)
    
    print(type(year_value))
    print(year_value)
    
    figure = go.Figure()
    
    #year_filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df = df[df["iyear"].isin(year_range)]
    
    #month_filter
    if month_value is None or month_value == []:
        pass
    else:
        if date_value is None or date_value == []:
                new_df = new_df[new_df["imonth"].isin(month_value)]
        else:
                new_df = new_df[(new_df["imonth"].isin(month_value)) &
                                 (new_df["iday"].isin(date_value))] 
            
        #region, country, state, city filters
        
        if region_value is None or region_value == []:
             pass
        else:
            if country_value is None or country_value == []:
                 new_df = new_df[(new_df["region_txt"].isin(region_value))]
                                                                
            else:
               if state_value is None or state_value == []:
                    new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                    (new_df["country_txt"].isin(country_value))]  
               else:   
                  if city_value is None or city_value == []:
                       new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                (new_df["country_txt"].isin(country_value)) &
                                (new_df["provstate"].isin(state_value))]
                  else:
                      new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                      (new_df["country_txt"].isin(country_value)) &
                                      (new_df["provstate"].isin(state_value)) &
                                      (new_df["city"].isin(city_value))]
        #attack_value      
        if attack_type_value is None or attack_type_value == []:
              pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_type_value)]       
            
    
        
        if new_df.shape[0]:
             pass
        else:
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday',
                                             'region_txt','country_txt','provstate','city',
                                             'latitude','longitude',
                                             'attacktype1_txt','nkill'])
    
            new_df.loc[0] = [0,0,0,None,None,None,None,None,None,None,None]
    
    
        figure = px.scatter_mapbox(new_df,
                               lat = "latitude",
                               lon = "longitude",
                               color = "attacktype1_txt",
                               hover_name = "city",
                               hover_data = [ 'region_txt','country_txt','provstate','city','attacktype1_txt','nkill','iyear'],
                               zoom = 1
                               )
                                              
        figure.update_layout(mapbox_style="stamen-toner",
                         
                         autosize = True,
                         margin = dict(l=0, r=0,t=25,b=20),
                        
                         )


       
    
  elif Tabs == "chart":
         
         year_range_chart = range(chart_year_selector[0], chart_year_selector[1]+1)
                             
         chart_df = df[df["iyear"].isin(year_range_chart)]
    
         if subtabs2 == "WorldChart":
            pass
         elif subtabs2 == "IndiaChart":
             chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &
                                 (chart_df["country_txt"]=="India")]
         if chart_dd_value is not None and chart_df.shape[0]:
                chart_df = chart_df.groupby("iyear") [chart_dd_value].value_counts().reset_index(name = "count")
                
        
         else:
             chart_df = chart_df.groupby('iyear')[chart_year_selector].value_counts().reset_index(name = "count")
         if chart_df.shape[0]:
             pass
         else:
            chart_df = pd.DataFrame(columns = ['iyear','count', chart_dd_value])
            chart_df.loc[0] = [0, 0, "No data"]
    
         figure = px.area(chart_df, x = "iyear", y = "count", color = chart_dd_value)                                       
    
  return dcc.Graph(figure = figure)



@app.callback(
    Output("date","options"),
    [
     Input("month","value")
     
     ]
    )
def update_date(month_value):
    date_list = [x for x in range (1, 32)]
    option = []
    if month_value:
         option = [{"label":m,"value":m} for m in date_list]
        
    return option
    
@app.callback(
     [
      Output("region_dropdown", "value"),
      Output("region_dropdown", "disabled"),
      Output("countr_dropdown", "value"),
      Output("country_dropdown", "disabled")],
      [Input("subtabs1", "value")]
      
    )    
def update_r(Tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if Tab == "WorldMap":
        pass
    elif Tab == "IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c
    
 
@app.callback(
    Output("country_dropdown","options"),
    [
     Input("region_dropdown","value")
     
     ]
    )   
    
def set_country_options(region_value):
    option = []
    if region_value is None:
         raise PreventUpdate
    
    else:
        for var in region_value:
            if var in country_list.keys():
                 option.extend(country_list[var])
    
    return  [{'label':m, 'value':m} for m in option]
@app.callback(
    Output("state_dropdown","options"),
    [
     Input("country_dropdown","value")
     
     ]
    )   
    
def set_state_options(country_value):
    option = []
    if country_value is None:
         raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                 option.extend(state_list[var])
    
    return  [{'label':m, 'value':m} for m in option]
    
@app.callback(
    Output("city_dropdown","options"),
    [
     Input("state_dropdown","value")
     
     ]
    )   
    
def set_city_options(state_value):
    option = []
    if state_value is None:
         raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                 option.extend(city_list[var])
    
    return  [{'label':m, 'value':m} for m in option]
    
"""    

"""


def run_browser():
    webbrowser.open_new('http://127.0.0.1:4050/')
    
    #Main function   
def main(): 

    print("Starting the main function")
 
    #calling_functions
    
    load_data()

    run_browser()
   
    
#layout controls the UI and Callback controls the Action

    global app
    app.layout = app_dashboard_ui()
    app.title = "Terrorism Analysis with Insights"
    
    app.run_server(port=4050)
    #don't write any statement after run_server function because it will cause no effect to the program
    df = None
    app = None
    print("Ending the main function")

   
   
if __name__ == '__main__':
    print("Starting the Project")
    main()
    print("Ending the Project")    