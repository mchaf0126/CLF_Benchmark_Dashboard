from math import log
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import pandas as pd
from src.components.dropdowns import create_dropdown
from src.components.toggle import create_toggle
from src.components.radio_items import create_radio_items
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

new_constr_toggle_yaml = config.get('new_constr_toggle_cont')
assert new_constr_toggle_yaml is not None, 'The config for new construction could not be set'

outlier_toggle_yaml = config.get('outlier_toggle_cont')
assert outlier_toggle_yaml is not None, 'The config for new construction could not be set'

floor_area_radio_yaml = config.get('floor_area_normalization_cont')
assert floor_area_radio_yaml is not None, 'The config for floor area norm. could not be set'

log_linear_dropdown_yaml = config.get('log_linear_dropdown')
assert log_linear_dropdown_yaml is not None, 'The config for log-linear could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

cfa_gfa_map = config.get('cfa_gfa_map')
assert cfa_gfa_map is not None, 'The config for cfa/gfa map could not be set'

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

new_constr_toggle = create_toggle(
    toggle_list=new_constr_toggle_yaml['toggle_list'],
    first_item=new_constr_toggle_yaml['first_item'],
    toggle_id=new_constr_toggle_yaml['toggle_id'],
)

outlier_toggle = create_toggle(
    toggle_list=outlier_toggle_yaml['toggle_list'],
    first_item=outlier_toggle_yaml['first_item'],
    toggle_id=outlier_toggle_yaml['toggle_id'],
)

floor_area_radio = create_radio_items(
    label=floor_area_radio_yaml['label'],
    radio_list=floor_area_radio_yaml['radio_list'],
    first_item=floor_area_radio_yaml['first_item'],
    radio_id=floor_area_radio_yaml['radio_id']
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
    className='mb-4'
)

controls_cont = dbc.Card(
    [
        continuous_dropdown,
        total_impact_dropdown,
        color_dropdown,
        floor_area_radio,
        log_linear_radio,
        new_constr_toggle,
        outlier_toggle
    ],
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
        Input('floor_area_normal_cont', 'value'),
        Input('new_constr_toggle_cont', 'value'),
        Input('outlier_toggle_cont', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_chart(cont_x,
                 objective,
                 color_value,
                 log_linear,
                 cfa_gfa_type,
                 new_constr_toggle_cont,
                 outlier_toggle_cont,
                 buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    units_map = {
        'eci': '(kgCO<sub>2</sub>e/m<sup>2</sup>)',
        'epi': '(kgNe/m<sup>2</sup>)',
        'api': '(kgSO<sub>2</sub>e/m<sup>2</sup>)',
        'sfpi': '(kgO<sub>3</sub>e/m<sup>2</sup>)',
        'odpi': '(CFC-11e/m<sup>2</sup>)',
        'nredi': '(MJ/m<sup>2</sup>)',
        'ec_per_occupant': '(kgCO<sub>2</sub>e/occupant)',
        'ec_per_res_unit': '(kgCO<sub>2</sub>e/residential unit)',
    }
    if new_constr_toggle_cont == [1]:
        df = df[df['bldg_proj_type'] == 'New Construction']

    cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
    objective_for_graph = cfa_gfa_mapping.get(objective)

    if outlier_toggle_cont == [1]:
        Q1_objective = df[objective_for_graph].quantile(0.25)
        Q3_objective = df[objective_for_graph].quantile(0.75)
        IQR_objective = Q3_objective - Q1_objective
        df = df[
            (df[objective_for_graph] < Q3_objective + 3 * IQR_objective)
            & (df[objective_for_graph] > Q1_objective - 3 * IQR_objective)
        ]
        Q1_cont = df[cont_x].quantile(0.25)
        Q3_cont = df[cont_x].quantile(0.75)
        IQR_cont = Q3_cont - Q1_cont
        df = df[
            (df[cont_x] < Q3_cont + 3 * IQR_cont)
            & (df[cont_x] > Q1_cont - 3 * IQR_cont)
        ]

    max_of_df = df[objective_for_graph].max()
    max_of_cont_x = df[cont_x].max()
    min_of_df = df[objective_for_graph].min()
    min_of_cont_x = df[cont_x].min()
    xshift = create_graph_xshift(max_value=max_of_cont_x)
    yshift = create_graph_xshift(max_value=max_of_df)
    log_flag = False
    if log_linear == 'Logarithmic':
        log_flag = True
        range_x_for_graph = [min_of_cont_x, max_of_cont_x + xshift]
        range_y_for_graph = [min_of_df, max_of_df + yshift]
    else:
        range_x_for_graph = [0, max_of_cont_x + xshift]
        range_y_for_graph = [0, max_of_df + yshift]
    if color_value == 'No color':
        color_value = None
        point_count = df[~df[[cont_x, objective_for_graph]].isna().any(axis=1)].shape[0]
    else:
        point_count = df[~df[[cont_x, objective_for_graph, color_value]].isna().any(axis=1)].shape[0]

    fig = px.scatter(
        df,
        x=cont_x,
        y=objective_for_graph,
        color=color_value,
        log_x=log_flag,
        log_y=log_flag,
        range_x=range_x_for_graph,
        range_y=range_y_for_graph,
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
        ],
        height=600
    )

    fig.update_xaxes(
        title=\
            f'{field_name_map.get(cont_x)} \
(n={point_count})',
        tickformat=',.2f',
        minor=dict(showgrid=True)
        )
    fig.update_yaxes(
        title=f'{field_name_map.get(objective_for_graph)} {units_map.get(objective)}',
        tickformat=',.2f',
        minor=dict(showgrid=True)
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
        Input('floor_area_normal_cont', 'value'),
        Input('new_constr_toggle_cont', 'value'),
        Input('outlier_toggle_cont', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_table(cont_value,
                 impact_value,
                 color_value,
                 cfa_gfa_type,
                 new_constr_toggle_cont,
                 outlier_toggle_cont,
                 buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    if new_constr_toggle_cont == [1]:
        df = df[df['bldg_proj_type'] == 'New Construction']

    cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
    impact_value_for_graph = cfa_gfa_mapping.get(impact_value)
    if color_value == 'No color':
        df = df[~df[[cont_value, impact_value_for_graph]].isna().any(axis=1)]
    else:
        df = df[~df[[cont_value, impact_value_for_graph, color_value]].isna().any(axis=1)]

    if outlier_toggle_cont == [1]:
        Q1 = df[impact_value_for_graph].quantile(0.25)
        Q3 = df[impact_value_for_graph].quantile(0.75)
        IQR = Q3 - Q1
        df = df[
            (df[impact_value_for_graph] < Q3 + 3 * IQR)
            & (df[impact_value_for_graph] > Q1 - 3 * IQR)
        ]

    valeformatter = {"function": "d3.format(',.2f')(params.value)"}
    if color_value == 'No color':
        data = df[
            [
                cont_value,
                impact_value_for_graph
            ]
        ].sort_values(by=cont_value).to_dict('records')
        cols = \
            [
                create_float_table_entry(
                    float_col,
                    field_name_map.get(float_col),
                    valeformatter
                ) for float_col in [cont_value, impact_value_for_graph]
            ]
    else:
        data = df[
            [cont_value, impact_value_for_graph, color_value]
        ].sort_values(by=color_value).to_dict('records')
        cols = (
            [create_string_table_entry(color_value, field_name_map.get(color_value))]
            + [
                create_float_table_entry(
                    float_col,
                    field_name_map.get(float_col),
                    valeformatter
                ) for float_col in [cont_value, impact_value_for_graph]
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
        State('floor_area_normal_cont', 'value'),
        State('new_constr_toggle_cont', 'value'),
        State('outlier_toggle_cont', 'value')
    ],
    prevent_initial_call=True,
)
def func(cont_value,
         impact_value,
         n_clicks,
         buildings_metadata,
         color_value,
         cfa_gfa_type,
         new_constr_toggle_cont,
         outlier_toggle_cont):
    if n_clicks > 0:
        df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))

        if new_constr_toggle_cont == [1]:
            df = df[df['bldg_proj_type'] == 'New Construction']

        cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
        impact_value_for_graph = cfa_gfa_mapping.get(impact_value)

        if outlier_toggle_cont == [1]:
            Q1 = df[impact_value_for_graph].quantile(0.25)
            Q3 = df[impact_value_for_graph].quantile(0.75)
            IQR = Q3 - Q1
            df = df[
                (df[impact_value_for_graph] < Q3 + 3 * IQR)
                & (df[impact_value_for_graph] > Q1 - 3 * IQR)
            ]

        if color_value == "No Color":
            return dcc.send_data_frame(
                df[[cont_value, impact_value_for_graph]].sort_values(by=cont_value).to_csv,
                f"{cont_value} values by {impact_value_for_graph}.csv",
                index=False)
        else:
            return dcc.send_data_frame(
                df[
                    [
                        color_value,
                        cont_value,
                        impact_value_for_graph
                    ]
                ].sort_values(by=color_value).to_csv,
                f"{cont_value} values by {impact_value_for_graph} sorted by {color_value}.csv",
                index=False)
