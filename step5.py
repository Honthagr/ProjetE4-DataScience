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
                "After testing multiple models, we can conclude that indeed, simpler linear models were better. This can be explained by the correlations previously evocated before but also by the size of the dataset. More complex model tend to need more data to have better generalization. One more reason that could explain such results could be hyperparameter tuning, more complex models can perform better with proper parameters. However, this requires a better machine in order to not take several hours (time taken in the attached notebook: about 5 hours)."
            ], className='row-content'),
            html.P([
                "In the end, the model standing above all the others is the Ridge regressor. Having both the best performance and a really good computation time (the one in the notebook indicates the computation time for the entire grid search of 140 fits). However, if the time is completely taken into account, linear regression wins the computation sprint with only a slightly worse score."
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