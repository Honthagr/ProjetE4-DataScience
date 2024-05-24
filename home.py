import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', title='Data Science | Home')

layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H3('Data Science'),
            html.P('ESIEE Paris', className='par')
        ], width=12, className='row-titles')
    ]),
    
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                html.B('Our project is divided into different stages:')
            ], className='guide'),
            html.P([
                html.B('1) Data pre-processing'),
                html.Br(),
                'As a first step, we filled in the gaps in our dataset to produce consistent training and test datasets.'
            ], className='guide'),
            html.P([
                html.B('2) Feature engineering and Data processing'),
                html.Br(),
                'After pre-processing our dataset, we focused on feature engineering and data processing.'
            ], className='guide'),
            html.P([
                html.B('3) Machine Learning & Deep Learning predictions'),
                html.Br(),
                'Then, we checked if these were reliable weather data prediction models.'
            ], className='guide'),
            html.P([
                html.B('4) Performances'),
                html.Br(),
                'Finally, in order to display our results, we chose some metrics to understand the performance of the trained models.'
            ], className='guide'),
            html.P([
                html.B('5) Conclusion'),
                html.Br(),
                'To conclude, we analized our results to identify the best model.'
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
    ]),
])