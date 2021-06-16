from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from app import app
from utils.database.orm_engine import db_session as db
from utils.database.models import MeasurementInfo
import utils.wavefront as wf_helper

import pandas as pd

from urllib.parse import urlparse, parse_qs

@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'),
    Input('url', 'href'),
)
def display_value(value, href):
    parts = urlparse(href)
    print(parts)
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output('zern-figure', 'figure'),
    Input('url', 'href'),
    Input({'type': 'dropdown', 'index': ALL}, 'value'),
    State({'type': 'dropdown', 'index': ALL}, 'id'),
)
def update_zern_figure(href, value, id):
    if not value or value[0] is None:
        idx = 0
    else:
        idx = int(value[0])

    parts = urlparse(href)
    query_dict = parse_qs(parts.query)
    mea_id = int(query_dict['id'][0])

    q = db.query(MeasurementInfo).filter(MeasurementInfo.id == mea_id)
    json_data = q[0].raw_data

    title_str = '{} Zernike Polynomials'.format(json_data['data'][idx]['sample_name'])
    fig = go.Figure(
        data=[go.Bar(
            x=['Power', 'Astigmatism X', 'Astigmatism Y', 'Coma X', 'Coma Y', 'Primary Spherical', 'Trefoil X', 'Trefoil Y', '2nd Astigmatism X' ,'2nd Astigmatism Y', '2nd Coma X', '2nd Coma Y', '2nd Spherical'],
            y=json_data['data'][idx]['zern_coeff'][3:16]
        )],
        layout_title_text=title_str,
    )

    fig.update_yaxes(title='OPD')

    return fig


@app.callback(
    Output('surface-figure', 'figure'),
    Input('wavefront-value', 'data'),
    Input({'type': 'dropdown', 'index': ALL}, 'value'),
    State({'type': 'dropdown', 'index': ALL}, 'id'),
)
def update_surface_figure(json_data, value, id):
    if not value or value[0] is None:
        idx = 0
    else:
        idx = int(value[0])

    _z, _x, _y = wf_helper.wf_evaluate_cart(json_data['data'][idx]['zern_coeff'])
    title_str = '{} Wavefront'.format(json_data['data'][idx]['sample_name'])
    fig = go.Figure(
        data = [go.Surface(
            x=_x,
            y=_y,
            z=_z,
            colorscale='JET',
        )],
        layout_title_text=title_str,
    )
    fig.update_layout(
        scene={
            'aspectratio': {"x": 2, "y": 2, "z": 0.5}
        }
    )

    return fig


@app.callback(
    Output('sample-index', 'children'),
    Input('wavefront-value', 'data'),
    State('sample-index', 'children'),
)
def update_dropdown(json_data, children: list):
    n_data = len(json_data['data'])
    mea_data = list()

    for idx in range(n_data):
        item = list()
        item.append(idx+1)
        if len(json_data['data'][idx]['sample_name']) == 0:
            item.append('{}-item'.format(idx))
        else:
            item.append(json_data['data'][idx]['sample_name'])
        item.append(json_data['data'][idx]['pv'])
        item.append(json_data['data'][idx]['rms'])
        item.append(json_data['data'][idx]['zern_pow'])

        mea_data.append(item)

    df = pd.DataFrame(mea_data, columns=['INDEX', 'NAME', 'PV', 'RMS', 'POWER'])

    surface_options = list()
    for i in range(n_data):
        item = {'label': df['NAME'][i], 'value': str(i)}
        surface_options.append(item)

    new_element = html.Div([
        dcc.Dropdown(
            id={
                'type': 'dropdown',
                'index': 0
            },
            options=surface_options
        ),
        html.Div(
            id={
                'type': 'output',
                'index': 0
            }
        )
    ])
    children.append(new_element)
    return children


@app.callback(
    Output('sample-table', 'figure'),
    Input('wavefront-value', 'data'),
)
def analysis_sample_table(json_data):
    n_data = len(json_data['data'])
    mea_data = list()

    for idx in range(n_data):
        item = list()
        item.append(idx+1)
        if len(json_data['data'][idx]['sample_name']) == 0:
            item.append('{}-item'.format(idx))
        else:
            item.append(json_data['data'][idx]['sample_name'])
        item.append(json_data['data'][idx]['pv'])
        item.append(json_data['data'][idx]['rms'])
        item.append(json_data['data'][idx]['zern_pow'])

        mea_data.append(item)

    df = pd.DataFrame(mea_data, columns=['INDEX', 'NAME', 'PV', 'RMS', 'POWER'])

    fig = go.Figure(data=go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[df.INDEX, df.NAME, df.PV, df.RMS, df.POWER],
                   fill_color='lavender',
                   align='center')
    ))

    return fig


@app.callback(
    Output('box-figure', 'figure'),
    Input('wavefront-value', 'data')
)
def analysis_box_plot(json_data):
    n_data = len(json_data['data'])
    mea_data = list()

    for idx in range(n_data):
        item = list()
        item.append(idx+1)
        if len(json_data['data'][idx]['sample_name']) == 0:
            item.append('{}-item'.format(idx))
        else:
            item.append(json_data['data'][idx]['sample_name'])
        item.append(json_data['data'][idx]['pv'])
        item.append(json_data['data'][idx]['rms'])
        item.append(json_data['data'][idx]['zern_pow'])

        mea_data.append(item)

    df = pd.DataFrame(mea_data, columns=['INDEX', 'NAME', 'PV', 'RMS', 'POWER'])

    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df['PV'],
        boxpoints='all',
        jitter=0.0,
        pointpos=-1.3,
        name='PV',
        hovertext=df["INDEX"],
    ))
    fig.add_trace(go.Box(
        y=df['RMS'],
        boxpoints='all',
        jitter=0.0,
        pointpos=-1.3,
        name='RMS',
        hovertext=df["INDEX"],
    ))
    fig.add_trace(go.Box(
        y=df['POWER'],
        boxpoints='all',
        jitter=0.0,
        pointpos=-1.3,
        name='POWER',
        hovertext=df["INDEX"],
    ))
    return fig


@app.callback(
    Output('wavefront-value', 'data'),
    Input('url', 'href'),
)
def load_data(href):
    parts = urlparse(href)
    query_dict = parse_qs(parts.query)
    mea_id = int(query_dict['id'][0])

    q = db.query(MeasurementInfo).filter(MeasurementInfo.id == mea_id)
    json_data = q[0].raw_data
    return json_data
