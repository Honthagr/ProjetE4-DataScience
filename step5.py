import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output,callback

dash.register_page(__name__, name='5-Conclusion', title='Data Science | Conclusion')

# New page
layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col([
            html.P([
                html.Br(),
                ])], width=2),
        dbc.Col([
            html.H3('Our conclusion')], width=12, className='row-titles')
    ]),
    
    dbc.Row([
        dbc.Col([
            html.P([
                "To conclude,..."
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
    ]),    
])