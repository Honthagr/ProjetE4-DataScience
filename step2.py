import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pmdarima.utils import diff
from statsmodels.tsa.stattools import adfuller

dash.register_page(__name__, name='2-Machine Learning & Deep Learning', title='Data Science | Machine Learning & Deep Learning')

layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                html.B(),
                html.Br(),
            ], className='guide'),
            html.P([
                html.B(),
                html.Br(),
            ], className='guide'),
            html.P([
                html.B(),
                html.Br(),
            ], className='guide')
        ], width=8),
        dbc.Col([], width=2)
    ]),
    
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                html.B('Our project is divided into different stages:')
            ], className='guide'),
            html.P([
                html.B('1) Data processing'),
                html.Br(),
                'To begin with, we filled in the gaps in our dataset. We then normalized our data. Finally, we retained only the most relevant features.'
            ], className='guide'),
            html.P([
                html.B('2) Machine Learning & Deep Learning'),
                html.Br(),
                'After processing our dataset, we selected a few algorithms that were consistent with it.'
            ], className='guide'),
            html.P([
                html.B('3) Predictions'),
                html.Br(),
                'Then, we checked if these were reliable weather data prediction models.'
            ], className='guide'),
            html.P([
                html.B('4) Performances'),
                html.Br(),
                'Finally, in order to display our results, we created a dashboard in Python language, making it easy to understand the performance of the trained models.'
            ], className='guide')
        ], width=8),
        dbc.Col([], width=2)
    ]),
    
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                html.B(),
                html.Br(),
            ], className='guide')
        ], width=8),
        dbc.Col([], width=2)
    ])
])