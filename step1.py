import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from assets.fig_layout import my_figlayout, my_linelayout

dash.register_page(__name__, name='1-Data processing', title='Data Science | Data processing')

_data_energy_avg_ = pd.read_csv('data/energy_avg_.csv', usecols=[2, 8], names=['valid_datetime', 'GSolar_MW'], skiprows=1)

_data_energy_avg_["Time"] = _data_energy_avg_["valid_datetime"]
_data_energy_avg_["GSolar_MW"] = _data_energy_avg_["GSolar_MW"]

# Mise en page de l'application Dash
layout = dbc.Container([
    # Titre
    dbc.Row([
        dbc.Col([html.H3(['Our dataset'])], width=12, className='row-titles')
    ]),

    # Sélecteur de jeu de données
    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([html.P(['Select a dataset:'], className='par')], width=2),
        dbc.Col([
            dcc.RadioItems(['energy_avg_'], value='energy_avg_', persistence=True, persistence_type='session', id='radio-dataset')
        ], width=4),
        dbc.Col([], width=3)
    ], className='row-content'),

    # Figure de données brute
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(id='p1_1-loading', type='circle', children=dcc.Graph(id='fig-pg1', className='my-graph'))
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content')
])

# Mise à jour de la figure
@callback(
    Output(component_id='fig-pg1', component_property='figure'),
    Input(component_id='radio-dataset', component_property='value')
)
def plot_data(value):
    fig = None

    if value == 'energy_avg_':
        _data = _data_energy_avg_

    fig = go.Figure(layout=my_figlayout)
    fig.add_trace(go.Scatter(x=_data['Time'], y=_data['GSolar_MW'], line=dict()))

    fig.update_layout(title='Dataset Linechart', xaxis_title='Time', yaxis_title='GSolar_MW', height = 500)
    fig.update_traces(overwrite=True, line=my_linelayout)

    return fig
