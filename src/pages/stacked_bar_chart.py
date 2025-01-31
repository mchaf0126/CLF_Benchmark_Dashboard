import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import pandas as pd
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable, \
    create_float_table_entry, create_string_table_entry, \
    create_int_table_entry
from src.utils.load_config import app_config


register_page(__name__, path='/stacked_bar_chart')

config = app_config

categorical_dropdown_yaml = config.get('categorical_dropdown')
assert categorical_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

categorical_dropdown = create_dropdown(
    label=categorical_dropdown_yaml['label'],
    dropdown_list=categorical_dropdown_yaml['dropdown_list'],
    first_item=categorical_dropdown_yaml['first_item'],
    dropdown_id=categorical_dropdown_yaml['dropdown_id']
)

total_impact_dropdown = create_dropdown(
    label=total_impact_dropdown_yaml['label'],
    dropdown_list=total_impact_dropdown_yaml['dropdown_list'],
    first_item=total_impact_dropdown_yaml['first_item'],
    dropdown_id='total_impact_dropdown_stacked'
)

controls_cont = dbc.Card(
    [categorical_dropdown, total_impact_dropdown],
    body=True,
)

table = create_datatable(table_id='results_table_stacked_bar')

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls_cont
                    ], xs=3, sm=3, md=2, lg=2, xl=2, xxl=2
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="stacked_bar"),
                    ], xs=7, sm=7, md=8, lg=8, xl=8, xxl=8
                ),
            ],
            justify='center',
            className='mb-4'
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.Button("Download Table Contents", id="btn-download-tbl-stack"),
                    dcc.Download(id="download-tbl-stack"),
                    table,
                ]),
                width={"size": 7},
            ),
            justify='center'
        ),
    ],
)


@callback(
    Output('stacked_bar', 'figure'),
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown_stacked', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_chart(cat_value, impact_type, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    fig = px.histogram(
        df,
        x=cat_value,
        y=impact_type,
        histfunc='avg'
    )
    fig.update_xaxes(
        title=cat_value,
        categoryorder='total descending'
        )
    fig.update_yaxes(
        title=f'Average Impacts by {impact_type} (kg CO2/m2)'
    )
    # fig.update_traces(
    #     marker=dict(
    #         color='#FDB525'
    #     ),
    #     textposition='auto'
    # )
    return fig


@callback(
    [
        Output('results_table_stacked_bar', 'columns'),
        Output('results_table_stacked_bar', 'data'),
        Output('results_table_stacked_bar', 'style_cell_conditional'),
        Output('results_table_stacked_bar', 'style_header_conditional'),
    ],
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown_stacked', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_table(cat_value, impact_value, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    impact_type = (impact_value)
    count_series = df.groupby(cat_value)[cat_value].count()
    cols = [create_string_table_entry(cat_value)] +\
        [create_int_table_entry('count')] + \
        [create_float_table_entry(c) for c in impact_type]

    data = (df.groupby(cat_value, as_index=False)[impact_type]
            .mean()
            .sort_values(by=cat_value)
            .assign(count=count_series.values)
            .to_dict('records')
            )
    style_cc = [
        {
            'if': {'column_id': impact_type+['count']},
            'textAlign': 'right',
            'minWidth': '70px', 'width': '70px', 'maxWidth': '70px',
        },
    ]
    style_head = [
        {
            'if': {'column_id': impact_type + ['count']},
            'textAlign': 'right',
        },
    ]
    return cols, data, style_cc, style_head


@callback(
    Output("download-tbl-stack", "data"),
    [
        State('categorical_dropdown', 'value'),
        State('total_impact_dropdown_stacked', 'value'),
        Input("btn-download-tbl-stack", "n_clicks"),
        State('buildings_metadata', 'data')
    ],
    prevent_initial_call=True,
)
def func(cat_value, impact_value, n_clicks, buildings_metadata):
    if n_clicks > 0:
        df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
        impact_type = (impact_value)
        count_series = df.groupby(cat_value)[cat_value].count()
        download_df = (df.groupby(cat_value, as_index=False)[impact_type]
                       .mean()
                       .assign(count=count_series.values)
                       .sort_values(by=cat_value)
                       )
        download_df = download_df[[cat_value]+['count']+impact_type]
        return dcc.send_data_frame(
            download_df.to_csv,
            f"{cat_value} values by {impact_value}.csv",
            index=False)
