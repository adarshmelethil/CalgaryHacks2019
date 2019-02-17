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
from datetime import datetime, timezone
import pytz

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


def add_time():
    new_date = []
    new_day = []
    new_hour = []
    new_minute =[]
    for index, row in df_crime_lat_lon.iterrows():
        timestamp = (row['time']/1000)
        dates = datetime.fromtimestamp(timestamp, pytz.timezone('Israel'))
        new_day.append(dates.day)
        new_hour.append(dates.hour)
        new_minute.append(dates.minute)

    df_crime_lat_lon['day'] = new_day

add_time()
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
    'background': '#FFFFFF',
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

        html.P('Showing crimes from categories: '.format(BINS),
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
                    height='800',
                ),
                style={"height": "80vh", "width": "100%"},
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
                    height=700
                )
            ),
            # animate = True
        )

    ], className='six columns', style={'margin': 0, 'height': 800}),

    html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        dcc.Graph(
            id='selected-data',
            figure=go.Figure(
                data=[go.Histogram(
                    histfunc = "count",
                    #cumulative=dict(enabled=True),
                    x=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Violence']['day'],
                    y=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Violence']['lon'],
                    name = "Violence"
                    ),
go.Histogram(
                    histfunc = "count",
                    #cumulative=dict(enabled=True),
                    x=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Breaking & Entering/Robbery']['day'],
                    y=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Breaking & Entering/Robbery']['lon'],
                    name = "Breaking&Entering/Robbery"
                    ),
go.Histogram(
                    histfunc = "count",
                    #cumulative=dict(enabled=True),
                    x=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Theft FROM Vehicle']['day'],
                    y=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Theft FROM Vehicle']['lon'],
                    name = "Theft from Vehicle"
                    ),

go.Histogram(
                    histfunc = "count",
                    #cumulative=dict(enabled=True),
                    x=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Illegal Drug Activity']['day'],
                    y=df_crime_lat_lon[df_crime_lat_lon['crime'] == 'Illegal Drug Activity']['lon'],
                    name = "count"
                    )

                ],
                layout=dict(
                    paper_bgcolor=colors['background'],
                    plot_bgcolor=colors['background'],
                    height=605,
                    title="Crime Per Day",
                    xaxis=dict(
                        title='Date of Current Month',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f'
                        )
                    ),
                    yaxis=dict(
                        title='Number of Crimes',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f'
                        )
                    )
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
    add_time()
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
    fig = dict(data=data, layout=layout)
    return fig


@app.callback(
    Output('heatmap-title', 'children'),
    [Input('crime-list', 'values')])
def update_map_title(crime):
    return 'Showing crimes from categories: {0}'.format(crime)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)