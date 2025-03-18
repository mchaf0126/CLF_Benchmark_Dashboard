from math import log
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import pandas as pd
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable, create_float_table_entry, \
    create_string_table_entry
from src.utils.load_config import app_config
from src.utils.general import create_graph_xshift

register_page(__name__, path='/scatter_plot')

config = app_config

continuous_dropdown_yaml = config.get('continuous_dropdown')
assert continuous_dropdown_yaml is not None, 'The config for cont. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

color_dropdown_yaml = config.get('color_dropdown')
assert color_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

log_linear_dropdown_yaml = config.get('log_linear_dropdown')
assert log_linear_dropdown_yaml is not None, 'The config for log-linear could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

continuous_dropdown = create_dropdown(
    label=continuous_dropdown_yaml['label'],
    dropdown_list=continuous_dropdown_yaml['dropdown_list'],
    first_item=continuous_dropdown_yaml['first_item'],
    dropdown_id=continuous_dropdown_yaml['dropdown_id']
)

total_impact_dropdown = create_dropdown(
    label=total_impact_dropdown_yaml['label'],
    dropdown_list=total_impact_dropdown_yaml['dropdown_list'],
    first_item=total_impact_dropdown_yaml['first_item'],
    dropdown_id=total_impact_dropdown_yaml['dropdown_id']
)

color_dropdown = create_dropdown(
    label=color_dropdown_yaml['label'],
    dropdown_list=color_dropdown_yaml['dropdown_list'],
    first_item=color_dropdown_yaml['first_item'],
    dropdown_id=color_dropdown_yaml['dropdown_id']
)

log_linear_radio = html.Div(
    [
        dbc.Label(log_linear_dropdown_yaml['label']),
        dbc.RadioItems(
            options=[
                {"label": "Linear", "value": 'linear'},
                {"label": "Logarithmic", "value": 'Logarithmic'},
            ],
            value='linear',
            id="log_linear_radio",
            inputCheckedClassName="border border-primary bg-primary"
        ),
    ],
)

controls_cont = dbc.Card(
    [continuous_dropdown, total_impact_dropdown, color_dropdown, log_linear_radio],
    body=True,
)

table = create_datatable(table_id='results_table_cont')

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls_cont
                    ], xs=4, sm=4, md=4, lg=4, xl=3, xxl=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="continuous_graph"),
                    ], xs=8, sm=8, md=8, lg=8, xl=7, xxl=7,
                ),
            ],
            justify='center',
            className='mb-4'
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                html.Div([
                    dbc.Button(
                        "Download Table Contents",
                        color='primary',
                        id="btn-download-tbl-scatter",
                        active=True,
                        className='my-2 fw-bold'
                    ),
                    dcc.Download(id="download-tbl-scatter"),
                    table,
                ]),
                xs=12, sm=12, md=8, lg=8, xl=8, xxl=8,
            ),
            justify='center',
            className='mb-4'
        ),
    ],
)


@callback(
    Output('continuous_graph', 'figure'),
    [
        Input('continuous_dropdown', 'value'),
        Input('total_impact_dropdown', 'value'),
        Input('color_dropdown', 'value'),
        Input('log_linear_radio', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_chart(cont_x, objective, color_value, log_linear, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    units_map = {
        'eci_a_to_c_gfa': '(kgCO2e/m2)',
        'epi_a_to_c_gfa': '(kgNe/m2)',
        'api_a_to_c_gfa': '(kgSO2e/m2)',
        'sfpi_a_to_c_gfa': '(kgO3e/m2)',
        'odpi_a_to_c_gfa': '(CFC-11e/m2)',
        'nredi_a_to_c_gfa': '(MJ/m2)',
        'ec_per_occupant_a_to_c': '(kgCO2e/occupant)',
        'ec_per_res_unit_a_to_c': '(kgCO2e/residential unit)',
    }
    max_of_df = df[cont_x].max()
    xshift = create_graph_xshift(max_value=max_of_df)
    log_flag = False
    if log_linear == 'Logarithmic':
        log_flag = True
        max_of_df = log(max_of_df + xshift, 10)
    else:
        max_of_df = max_of_df + xshift
    if color_value == 'No color':
        color_value = None

    fig = px.scatter(
        df,
        x=cont_x,
        y=objective,
        color=color_value,
        log_x=log_flag,
        log_y=log_flag,
        color_discrete_sequence=[
            "#32006e",
            "#e8e3d3",
            "#aadb1e",
            "#ffc700",
            "#2ad2c9",
            "#85754d",
            "#e93cac",
            "#4b2e83",
            '#c5b4e3'
        ]
    )
    fig.update_xaxes(
        title=f'{field_name_map.get(cont_x)} (n={df[~df[objective].isna()].shape[0]})',
        range=[0, max_of_df],
        tickformat=',.0f',
        )
    fig.update_yaxes(
        title=f'{field_name_map.get(objective)} {units_map.get(objective)}',
        tickformat=',.0f',
    )
    fig.update_layout(
        margin={'pad': 10},
        legend_title=None
    )
    return fig


@callback(
    [
        Output('results_table_cont', 'columnDefs'),
        Output('results_table_cont', 'rowData'),
    ],
    [
        Input('continuous_dropdown', 'value'),
        Input('total_impact_dropdown', 'value'),
        Input('color_dropdown', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_table(cont_value, impact_value, color_value, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    valeformatter = {"function": "d3.format(',.2f')(params.value)"}
    if color_value == 'No color':
        data = df[[cont_value, impact_value]].sort_values(by=cont_value).to_dict('records')
        cols = \
            [
                create_float_table_entry(
                    float_col,
                    field_name_map.get(float_col),
                    valeformatter
                ) for float_col in [cont_value, impact_value]
            ]
    else:
        data = df[
            [cont_value, impact_value, color_value]
        ].sort_values(by=color_value).to_dict('records')
        cols = (
            [create_string_table_entry(color_value, field_name_map.get(color_value))]
            + [
                create_float_table_entry(
                    float_col,
                    field_name_map.get(float_col),
                    valeformatter
                ) for float_col in [cont_value, impact_value]
              ]
        )
    return cols, data


@callback(
    Output("download-tbl-scatter", "data"),
    [
        State('continuous_dropdown', 'value'),
        State('total_impact_dropdown', 'value'),
        Input("btn-download-tbl-scatter", "n_clicks"),
        State('buildings_metadata', 'data'),
        State('color_dropdown', 'value'),
    ],
    prevent_initial_call=True,
)
def func(cont_value, impact_value, n_clicks, buildings_metadata, color_value):
    if n_clicks > 0:
        df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
        if color_value == "No Color":
            return dcc.send_data_frame(
                df[[cont_value, impact_value]].sort_values(by=cont_value).to_csv,
                f"{cont_value} values by {impact_value}.csv",
                index=False)
        else:
            return dcc.send_data_frame(
                df[[color_value, cont_value, impact_value]].sort_values(by=color_value).to_csv,
                f"{cont_value} values by {impact_value} sorted by {color_value}.csv",
                index=False)
