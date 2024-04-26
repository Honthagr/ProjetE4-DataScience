from dash import html
import dash_bootstrap_components as dbc

_footer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Hr([], className='hr-footer')], width=12)
        ]),
        dbc.Row([
            dbc.Col(['Created with Plotly Dash'], width=3),
            dbc.Col([], width=12),
            dbc.Col(['Océane BOURGEOIS, Nicolas CHARPENTIER, Franck JIANG, Antoine MERLET, Paul JUREK, Dominik VACA'], width=0, style={'text-align': 'right'}),
        ])
    ], fluid=True)
], className='footer')
