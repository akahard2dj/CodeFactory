import dash_core_components as dcc
import dash_html_components as html
import dash_table

layout_wavefront_report = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
])

layout_wavefront_individual = html.Div([
    html.Div([
        dcc.Store(id='wavefront-value'),
        html.Div([
            html.H3('Measurement Summary'),
            dcc.Graph(id='box-figure'),
            dcc.Graph(id='sample-table')
        ], className="six columns"),

        html.Div([
            html.H3('Wavefront Analysis'),
            html.Div(id='sample-index', children=[]),
            dcc.Graph(id='surface-figure'),
            dcc.Graph(id='zern-figure')
        ], className="six columns"),
    ], className="row")
])
