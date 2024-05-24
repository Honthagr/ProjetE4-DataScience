import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pmdarima.utils import diff
from statsmodels.tsa.stattools import adfuller

dash.register_page(__name__, name='2-Feature engineering and Data processing', title='Data Science | Features engineering and Data processing')

layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Br()
            ], width=2),
        dbc.Col([html.H3('Feature engineering & Data processing')], width=12, className='row-titles')
    ]),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                "Now that our datasets are assembled and split in training and test sets, we can focus on feature engineering and data processing."
            ], className='row-content'),
            html.P([
                'We start by dropping some columns that are either meaningless ("Unnamed: 0") or duplicates of other columns ("added_time"/"time"). However, even though "time" can be considered a repetition of "dtm", separating the different scales of time in this column looked like a good idea.'
            ], className='row-content'),
            html.P([
                'Next, we check colinearity between variables. Indeed, variables with high (or low) correlation may hinder the learning algorihtm, by increasing standard deviation in the process or making regression coefficients unstable. By doing that, we get rid of some varialbes such as "Solar_installedcapacity_mwp" or "dtm_year".'
            ], className='row-content'),
            html.P([
                'Then, we look for outliers. Those aberrant values may lead the learning algorithm in the wrong way, creating unintented biases. In this case, some were kept, some others not (randomness, minority, could not be explained).'
            ], className='row-content'),
            html.P([
                'At last, came the encoding of non-numerical values ("dtm_month-day" and "dtm_hour-minute") and scaling, in order to not have variables be overlooked by others with higher scale.'
            ], className='row-content'),
            html.P([
                html.Br(),
                'We then separate the labels "Solar_MW" from the features. The selection, elaboration and training of models can now start.'
            ], className='row-content')
        ], width=14),
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