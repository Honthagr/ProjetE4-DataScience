import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output,callback

dash.register_page(__name__, name='4-Performances', title='Data Science | Performances')

# Creation of the options' list
df = pd.read_csv('data/metrics.csv')
algorithm_options = [{'label': algo, 'value': algo} for algo in df['Algorithm']]
metric_options = [{'label': metric, 'value': metric} for metric in df.columns[1:]]


# New page
layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col([html.H3('Our results')], width=12, className='row-titles')
    ]),
    
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.P([
                html.B('Select an algorithm :')
            ], className='guide'),
            dcc.Dropdown(
                id='algorithm-dropdown',
                options=algorithm_options,
                value=algorithm_options[0]['value'],  # Initial value
                style={'width': '100%'}
            ),
            html.Br(),
            html.P([
                html.B('Select a metric :')
            ], className='guide'),
            dcc.Dropdown(
                id='metric-dropdown',
                options=metric_options,
                value=metric_options[0]['value'],  # Valeur initiale
                style={'width': '100%'}
            ),
            html.Br(),
            html.Div(id='display-selected-metric')
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
    
    dbc.Row([
        dbc.Col([
            html.P([
                html.Br(),
                ])], width=2),
        dbc.Col([html.H3('Our work')], width=12, className='row-titles'),
        dbc.Col([
            html.P([
                "In our case we have a regression problem. As such we need some special metrics to determine how good our models are."
            ], className='row-content'),
            html.P([
                html.Br(),
                "First we picked Mean Squared Error (MSE), it's the average of the squared differences between predicted and expected target values in a dataset. This value only grow bigger as the difference increases. That's why this metrics is used to punish bad model, and is good to determine if a model is good or not."
            ], className='row-content'),
            html.P([
                "Second we have the Mean Absolute Error (MAE). This metrics at the opposite of MSE grow linearly, and allow us to determine specifically the average error we have in our model. As we calculated weather information, it can tell us the error we have in average each days predicted."
            ], className='row-content'),
            html.P([
                "Thirdly we have the Median Absolute Error, at the difference of the MAE, this one take the median and not the mean, the difference will be that the outliers will be ignored. Comparing both can tell us if we have a lot of outliers, or if they impact a lot the results of the models."
            ], className='row-content'),
            html.P([
                "Finally we also choose R-Squared. This allow is to have a general indication if how good our models performed in term of pourcentage. Even if the result is not the accuracy of the model, it's still a good reference to take to determine how good a model is performing."
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

# Afficher la valeur de la métrique correspondant à l'algorithme sélectionné
@callback(
    Output('display-selected-metric', 'children'),
    [Input('algorithm-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def display_selected_metric(selected_algorithm, selected_metric):
    if selected_algorithm and selected_metric:
        selected_value = df[df['Algorithm'] == selected_algorithm][selected_metric].values[0]
        return f"The {selected_metric} value for {selected_algorithm} is : {selected_value}"
    else:
        return ""
