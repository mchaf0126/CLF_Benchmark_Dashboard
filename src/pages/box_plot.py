import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable, \
    create_float_table_entry, create_string_table_entry, create_int_table_entry
from src.utils.load_config import app_config
from src.utils.general import create_graph_xshift

config = app_config

register_page(__name__, path='/box_plot')

categorical_dropdown_yaml = config.get('categorical_dropdown')
assert categorical_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'


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
    dropdown_id=total_impact_dropdown_yaml['dropdown_id']
)

controls_cat = dbc.Card(
    [categorical_dropdown, total_impact_dropdown],
    body=True,
)

table = create_datatable(table_id='results_table_cat')

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls_cat
                    ], xs=4, sm=4, md=4, lg=4, xl=3, xxl=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="categorical_graph")
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
                        id="btn-download-tbl-box",
                        active=True,
                        className='my-2 fw-bold'
                    ),
                    dcc.Download(id="download-tbl-box"),
                    table,
                ]),
                xs=12, sm=12, md=12, lg=12, xl=8, xxl=8,
            ),
            justify='center',
            className='mb-4'
        )
    ],
)


@callback(
    Output('categorical_graph', 'figure'),
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_chart(category_x, objective, buildings_metadata):
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

    max_of_df = df[objective].max()
    xshift = create_graph_xshift(max_value=max_of_df)

    grouped_medians = (
        df[[category_x, objective]]
        .groupby(by=category_x)
        .median()
        .sort_values(
            by=objective,
            ascending=False
        )
    )
    order_by_median = grouped_medians.index.to_list()
    fig = px.box(
        df,
        y=category_x,
        x=objective,
        category_orders={
            category_x: order_by_median
        },
        color_discrete_sequence=["#ffc700"]

    )
    for s in df[category_x].unique():
        if len(df[df[category_x] == s]) > 0:
            fig.add_annotation(
                y=str(s),
                x=max_of_df+xshift,
                text=f'n={str(len(df[df[category_x]==s][category_x]))}',
                showarrow=False
            )
    fig.update_xaxes(
        title=field_name_map.get(objective) + f' {units_map.get(objective)}',
        range=[0, max_of_df+xshift],
        tickformat=',.0f',
        )
    fig.update_yaxes(
        title=field_name_map.get(category_x),
        tickformat=',.0f',
    )
    fig.update_traces(
        quartilemethod='inclusive',
    )
    fig.update_layout(
        margin={'pad': 10},
    )
    return fig


@callback(
    [
        Output('results_table_cat', 'columnDefs'),
        Output('results_table_cat', 'rowData'),
    ],
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_table(cat_value, impact_value, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    df[cat_value] = df[cat_value].fillna('NULL')

    tbl_df = (
        df.groupby(
            cat_value, as_index=False
        )[impact_value]
        .describe()
        .rename(
            columns={
                '25%': 'Q1',
                '50%': 'median',
                '75%': 'Q3'
            }
        ).drop(
            columns='count'
        )
    )
    tbl_df = pd.merge(
        left=tbl_df,
        right=df[cat_value].value_counts(),
        how='left',
        left_on=cat_value,
        right_on=cat_value
    )

    float_columns = [
        'mean',
        'std',
        'max',
        'min',
        'median',
        'Q1',
        'Q3'
    ]

    if impact_value in ['epi_a_to_c_gfa', 'api_a_to_c_gfa', 'sfpi_a_to_c_gfa']:
        valueformatter = {"function": "d3.format(',.2f')(params.value)"}
    elif impact_value == 'odpi_a_to_c_gfa':
        valueformatter = {"function": "d3.format(',.5f')(params.value)"}
    else:
        valueformatter = {"function": "d3.format(',.0f')(params.value)"}

    cols = (
        [create_string_table_entry(cat_value, field_name_map.get(cat_value))]
        + [create_int_table_entry('count')]
        + [
            create_float_table_entry(
                float_col, field_name_map.get(float_col), valueformatter
            ) for float_col in float_columns
          ]
    )
    data = tbl_df.to_dict('records')
    return cols, data


@callback(
    Output("download-tbl-box", "data"),
    [
        Input("btn-download-tbl-box", "n_clicks"),
        State('categorical_dropdown', 'value'),
        State('total_impact_dropdown', 'value'),
        State('buildings_metadata', 'data')
    ],
    prevent_initial_call=True,
)
def func(n_clicks, cat_value, impact_value, buildings_metadata):
    if n_clicks > 0:
        df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))

        tbl_df = (
            df.groupby(
                cat_value, as_index=False
            )[impact_value]
            .describe()
            .rename(
                columns={
                    '25%': 'Q1',
                    '50%': 'median',
                    '75%': 'Q3'
                }
            )
        )
        return dcc.send_data_frame(
            tbl_df.to_csv,
            f"{cat_value} values by {impact_value}.csv",
            index=False)
