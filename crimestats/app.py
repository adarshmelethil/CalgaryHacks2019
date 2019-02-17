# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_colorscales
import pandas as pd
import cufflinks as cf
import numpy as np
import re
import pymongo

app = dash.Dash(__name__)
server = app.server

app.config["APPLICATION_ROOT"] = "/statistic"

#df_crime_lat_lon = pd.read_csv('export.csv')

mongo_addr = os.environ.get("MONGO_URI") or "mongodb://localhost:27017"
myclient = pymongo.MongoClient(mongo_addr)

mydb = myclient["hackdb"]
crimeconnect = mydb.crimes
df_crime_lat_lon = pd.DataFrame(list(crimeconnect.find()))
if '_id' in df_crime_lat_lon:
    del df_crime_lat_lon['_id']


YEARS = [2013, 2014, 2015]

BINS = ['Violence', 'B&E/Robbery', 'Theft FROM Vehicle', 'Illegal Drug Activity']

DEFAULT_COLORSCALE = ["#2a4858", "#00968e", "#64c988", "#fafa6e"]

DEFAULT_OPACITY = 0.8

# DEFAULT_COLORSCALE = reversed(DEFAULT_COLORSCALE)

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.Div([
        html.Div([
            html.Div([
                html.H4(children='CrimeFinder - Dashboard'),
                html.P('Check boxes to filter through categories:'),
            ]),

            html.Div([
                dcc.Checklist(
                    id = 'crime-list',
                    options=[
                        {'label': 'Violence/Personal Theft', 'value': 'Violence'},
                        {'label': 'Breaking & Entering/Robbery', 'value': 'Breaking & Entering/Robbery'},
                        {'label': 'Theft from Vehicle', 'value': 'Theft FROM Vehicle'},
                        {'label': 'Illegal Drug Activity', 'value': 'Illegal Drug Activity'}
                    ],
                    values=['Violence']
                ),
            ], style={'width': 400, 'margin': 0}),
html.Div([
    html.Button('Refresh', id='btn-1', n_clicks_timestamp='0'),
    html.Div(id='container-button-timestamp')
]),

            html.Br(),
        ], style={'margin': 20}),

        html.P('Showing crimes from categories: '.format(min(YEARS)),
               id='heatmap-title',
               style={'fontWeight': 600}
               ),

        dcc.Graph(
            id='city-crimes',
            figure=dict(
                data=dict(
                    lat=(df_crime_lat_lon['lat'] if 'lat' in df_crime_lat_lon else []),
                    lon=(df_crime_lat_lon['lon'] if 'lon' in df_crime_lat_lon else []),
                    text=(df_crime_lat_lon['crime'] if 'crime' in df_crime_lat_lon else []),
                    type='scattermapbox'
                ),
                layout=dict(
                    mapbox=dict(
                        layers=[],
                        accesstoken=mapbox_access_token,
                        style='light',
                        center=dict(
                            lat=51.05,
                            lon=-114.07,
                        ),
                        pitch=0,
                        zoom=9.5
                    ),
height=800
                )
            )
        ),

        html.Div([
            html.P('Statistics are from the Previous Week'
                   )
        ], style={'margin': 20}),
        dcc.Graph(
            id='selected-data2',
            figure=dict(
                data=[dict(x=0, y=0)],
                layout=dict(
                    paper_bgcolor=colors['background'],
                    plot_bgcolor=colors['background'],
                    height=720
                )
            ),
            # animate = True
        )

    ], className='six columns', style={'margin': 0}),

    html.Div([
        dcc.Checklist(
            options=[{'label': 'Log scale', 'value': 'log'},
                     {'label': 'Hide legend', 'value': 'hide_legend'},
                     {'label': 'Include values flagged "Unreliable"', 'value': 'include_unreliable'}],
            values=[],
            labelStyle={'display': 'inline-block'},
            id='log-scale',
            style={'position': 'absolute', 'right': 80, 'top': 10}
        ),
        html.Br(),
        html.P('Select chart:', style={'display': 'inline-block'}),
        dcc.Dropdown(
            options=[{'label': 'Histogram of total number of deaths (single year)', 'value': 'show_absolute_deaths_single_year'},
                     {'label': 'Histogram of total number of deaths (1999-2016)', 'value': 'absolute_deaths_all_time'},
                     {'label': 'Age-adjusted death rate (single year)', 'value': 'show_death_rate_single_year'},
                     {'label': 'Trends in age-adjusted death rate (1999-2016)', 'value': 'death_rate_all_time'}],
            value='show_death_rate_single_year',
            id='chart-dropdown'
        ),
        dcc.Graph(
            id='selected-data',
            figure=dict(
                data=[dict(x=0, y=0)],
                layout=dict(
                    paper_bgcolor=colors['background'],
                    plot_bgcolor=colors['background'],
                    height=700
                )
            ),
            # animate = True
        ),
        dcc.Graph(
            id='selected-data1',
            figure=dict(
                data=[dict(x=0, y=0)],
                layout=dict(
                    paper_bgcolor=colors['background'],
                    plot_bgcolor=colors['background'],
                    height=700
                )
            ),
            # animate = True
        )
    ], className='six columns', style={'margin': 0}),
])

app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})

@app.callback(Output('container-button-timestamp', 'children'),
              [Input('btn-1', 'n_clicks')])
def displayClick(btn1):
    myclient = pymongo.MongoClient(mongo_addr)
    mydb = myclient["hackdb"]
    crimeconnect = mydb.crimes
    df_crime_lat_lon = pd.DataFrame(list(crimeconnect.find()))
    if "_id" in df_crime_lat_lon:
        del df_crime_lat_lon['_id']
    print("dang")
    print(df_crime_lat_lon.to_string)
    return

@app.callback(
    Output('city-crimes', 'figure'),
    [Input('crime-list', 'values')],
    [State('city-crimes', 'figure')])
def display_map(values, figure):
    cm = dict(zip(BINS, DEFAULT_COLORSCALE))
    data = []
    i=0
    print(values)
    for value in values:
        if 'crime' in df_crime_lat_lon:
            dataframe = df_crime_lat_lon[df_crime_lat_lon['crime'] == value]
            trace0 = go.Scattermapbox(
                lat=dataframe['lat'],
                lon=dataframe['lon'],
                text=dataframe['crime'],
                hoverinfo='text',
                mode='markers',
                name=value,
                # selected = dict(marker = dict(opacity=1)),
                # unselected = dict(marker = dict(opacity = 0)),
                marker=dict(size=9, color=DEFAULT_COLORSCALE[i])
            )
            data.append(trace0)
            i += 1
            if i >= 4:
                i = 0
    """
    annotations = [dict(
        showarrow=False,
        align='right',
        text='<b>Crime Category</b>',
        x=0.95,
        y=0.95,
    )]

    for i, bin in enumerate((BINS)):
        color = cm[bin]
        print(color)
        print(bin)
        annotations.append(
            dict(
                arrowcolor=color,
                text=bin,
                x=0.95,
                y=0.85 - (i / 4),
                ax=-80,
                ay=0,
                arrowwidth=5,
                arrowhead=0,
                bgcolor='#EFEFEE'
            )
        )
    """

    if 'layout' in figure:
        lat = figure['layout']['mapbox']['center']['lat']
        lon = figure['layout']['mapbox']['center']['lon']
        zoom = figure['layout']['mapbox']['zoom']
    else:
        lat = 51.05,
        lon = -114.07,
        zoom = 9.5

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style='light',
            center=dict(lat=lat, lon=lon),
            zoom=zoom
        ),
        hovermode='closest',
        margin=dict(r=0, l=0, t=0, b=0),
        #annotations=annotations,
        dragmode='lasso'
    )
    """
    base_url = 'https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/'
    for bin in BINS:
        geo_layer = dict(
            sourcetype='geojson',
            source=base_url + str(year) + '/' + bin + '.geojson',
            type='fill',
            color=cm[bin],
            opacity=DEFAULT_OPACITY
        )
        layout['mapbox']['layers'].append(geo_layer)
    """
    fig = dict(data=data, layout=layout)
    return fig


@app.callback(
    Output('heatmap-title', 'children'),
    [Input('crime-list', 'values')])
def update_map_title(crime):
    return 'Showing crimes from categories: {0}'.format(crime)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
