import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output,callback

dash.register_page(__name__, name='4-Mesures', title='Data Science | Résultats')

# Lecture du fichier CSV
df = pd.read_csv('data/metrics.csv')

# Création des options pour les menus déroulants des colonnes


# Création des options pour les menus déroulants des colonnes
algorithm_options = [{'label': algo, 'value': algo} for algo in df['Algorithm']]

# Création des options pour les menus déroulants des métriques
metric_options = [{'label': metric, 'value': metric} for metric in df.columns[1:]]


# Création de la nouvelle page
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
                html.B('Sélectionnez un algorithme :')
            ], className='guide'),
            dcc.Dropdown(
                id='algorithm-dropdown',
                options=algorithm_options,
                value=algorithm_options[0]['value'],  # Valeur initiale
                style={'width': '100%'}
            ),
            html.Br(),
            html.P([
                html.B('Sélectionnez une métrique :')
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
    ])
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
        return f"La valeur de {selected_metric} pour {selected_algorithm} est : {selected_value}"
    else:
        return ""
