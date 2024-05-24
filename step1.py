import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from assets.fig_layout import my_figlayout, my_linelayout

dash.register_page(__name__, name='1-Data pre-processing', title='Data Science | Data pre-processing')

_clean_solar_energy_train_ = pd.read_csv('data/clean_solar_energy_train.csv', usecols=[1, 6], names=['added_time', 'Solar_MW'], skiprows=1)
_clean_solar_energy_train_["Time"] = _clean_solar_energy_train_["added_time"]
_clean_solar_energy_train_["Solar_MW"] = _clean_solar_energy_train_["Solar_MW"]

_clean_solar_energy_test_ = pd.read_csv('data/clean_solar_energy_test.csv', usecols=[1, 6], names=['added_time', 'Solar_MW'], skiprows=1)
_clean_solar_energy_test_["Time"] = _clean_solar_energy_test_["added_time"]
_clean_solar_energy_test_["Solar_MW"] = _clean_solar_energy_test_["Solar_MW"]

# New page
layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col([html.H3('Data pre-processing')], width=12, className='row-titles')
    ]),

    # Dataset selection
    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([html.P('Select a dataset:', className='par')], width=2),
        dbc.Col([
            dcc.RadioItems(
                options=[
                    {'label': 'Training data', 'value': 'Training data'},
                    {'label': 'Testing data', 'value': 'Testing data'}
                ],
                value='Training data',
                persistence=True,
                persistence_type='session',
                id='radio-dataset'
            )
        ], width=4),
        dbc.Col([], width=3)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(id='loading', type='circle', children=dcc.Graph(id='plot_data', className='my-graph'))
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([
            html.P([
                html.Br(),
                ])], width=2),
        dbc.Col([html.H3('Our work')], width=12, className='row-titles'),
        dbc.Col([
            html.P([
                'In our study, we use two datasets. The first dataset is a CSV file containing solar and wind energy production data spanning three years. The second dataset includes meteorological measurements such as Solar Downward Radiation or temperature.'
            ], className='row-content'),
            html.P([
                html.Br(),
                'Our goal is to predict solar energy output using meteorological measurements through various machine learning models. Since our focus is only on predicting solar energy output, we will exclude columns that are not pertinent to our study. Specifically, we will remove the following columns:'
            ], className='row-content'),
            html.P([
                '• "MIP", "SS_Price", and "DA_Price" as they relate to pricing and do not influence solar energy production.'
            ], className='row-content'),
            html.P([
                '• "Wind_MW" and "boa_MWh" because we are not considering wind energy in this analysis.'
            ], className='row-content'),
            html.P([
                'By refining our dataset to include only relevant information, we can ensure that our machine learning models are more accurate and effective in predicting solar energy output, also lighter data can make improve our model’s performance.'
            ], className='row-content'),
            html.P([
                html.Br(),
                'Then, if we take a closer look at the SolarDownwardRadiation, Temperature and CloudCover columns, taken from meteorological data, we can see many variations. But if we consider the significance of this measurement, it should be continuous or at least show few variations, as solar radiation does not generally flash all day long. For this reason, we can consider a moving average to smooth out the variations and better capture the trends in solar radiation.'
            ], className='row-content'),
            html.P([
                html.Br(),
                "Let’s take a look at solar radiation :"
            ], className='row-content'),
            html.P([
                "First, we can notice that ref_datetime has periodicity of 6h. Indeed, these data comes from forecast every 6h. Also, we can notice that valid_datetime is an integer which is the period of the forecast. Since a whole forecast exceed 6h (120*30min= 60h) we can remove some forecast values, for instance forecast greater than 50h. It makes sense as forecast tend to be less precise over time which may decrease our models’ precision."
            ], className='row-content'),
            html.P([
                "After this first removal, we end up with multiple overlapping forecasts on some dates, so we can take the mean of these forecasts for each date."
            ], className='row-content'),
            html.P([
                html.Br(),
                "Next, we must address missing values :"
            ], className='row-content'),
            html.P([
                "We can observe 66 missing values for SolarMW which is not a significative amount so we can consider removing these missing values from our dataset. "
            ], className='row-content'),
            html.P([
                "However we will try to fill them instead. Since solar energy production usually depends on time, we can approximate Solar_MW by its mean grouped by time (hh:mm:ss)."
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

# Display the graph according to the selected dataset
@callback(
    Output('plot_data', 'figure'),
    [Input('radio-dataset', 'value')]
)
def plot_data(value):
    if value == 'Training data':
        _data = _clean_solar_energy_train_
    elif value == 'Testing data':
        _data = _clean_solar_energy_test_
    else:
        _data = pd.DataFrame(columns=["Time", "Solar_MW"])  # fallback in case of unexpected value

    fig = go.Figure(layout=my_figlayout)
    fig.add_trace(go.Scatter(x=_data['Time'], y=_data['Solar_MW'], line=dict()))

    fig.update_layout(title='Dataset Linechart', xaxis_title='Time', yaxis_title='Solar_MW', height=500)
    fig.update_traces(overwrite=True, line=my_linelayout)

    return fig
