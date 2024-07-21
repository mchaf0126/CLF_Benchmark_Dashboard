from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import src.utils.general as utils
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable, \
    create_float_table_entry, create_string_table_entry, \
    create_int_table_entry

register_page(__name__, path='/box_plot')

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
data_directory = main_directory.joinpath('data/public_dataset_fake_07-10-2024.csv')

df = pd.read_csv(data_directory, index_col=False)

config_path = main_directory.joinpath('src/components/config.yml')

config = utils.read_yaml(config_path)
assert config is not None, 'The config dictionary could not be set'

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
                    ], xs=3, sm=3, md=2, lg=2, xl=2, xxl=2
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="categorical_graph")
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
                    html.Button("Download Table Contents", id="btn-download-tbl-box"),
                    dcc.Download(id="download-tbl-box"),
                    table,
                ]),
                width={"size": 8},
            ),
            justify='center'
        )
    ],
)


@callback(
    Output('categorical_graph', 'figure'),
    Input('categorical_dropdown', 'value'),
    Input('total_impact_dropdown', 'value')
)
def update_chart(category_x, objective):
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
        }
    )
    for s in df[category_x].unique():
        fig.add_annotation(y=str(s),
                           x=4550,
                           text=f'n={str(len(df[df[category_x]==s][category_x]))}',
                           xshift=50,
                           showarrow=False
                           )
    fig.update_xaxes(
        title=objective + ' (kg CO2/m2)'
        )
    fig.update_yaxes(
        title=category_x
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
        Output('results_table_cat', 'columns'),
        Output('results_table_cat', 'data'),
        Output('results_table_cat', 'style_cell_conditional'),
        Output('results_table_cat', 'style_header_conditional')
    ],
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown', 'value')
    ]
)
def update_table(cat_value, impact_value):
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
    int_columns = [
        'count'
    ]
    float_columns = [
        'mean',
        'std',
        'max',
        'min',
        'median',
        'Q1',
        'Q3'
    ]
    number_cols = int_columns + float_columns

    tbl_df_cols = [cat_value] + number_cols
    tbl_df = tbl_df[tbl_df_cols]

    cols = [create_string_table_entry(cat_value)] + \
        [create_int_table_entry(int_col) for int_col in int_columns] + \
        [create_float_table_entry(float_col) for float_col in float_columns]
    data = tbl_df.to_dict('records')
    style_cc = [
        {
            'if': {'column_id': number_cols},
            'textAlign': 'right',
            'minWidth': '150 px', 'width': '150px', 'maxWidth': '150px',
        },
    ]
    style_head = [
        {
            'if': {'column_id': number_cols},
            'textAlign': 'right',
        },
    ]
    return cols, data, style_cc, style_head


@callback(
    Output("download-tbl-box", "data"),
    State('categorical_dropdown', 'value'),
    State('total_impact_dropdown', 'value'),
    Input("btn-download-tbl-box", "n_clicks"),
    prevent_initial_call=True,
)
def func(cat_value, impact_value, n_clicks):
    if n_clicks > 0:
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
        tbl_df = tbl_df[
            [
                cat_value,
                'count',
                'mean',
                'std',
                'max',
                'min',
                'median',
                'Q1',
                'Q3'
            ]
        ]
        return dcc.send_data_frame(
            tbl_df.to_csv,
            f"{cat_value} values by {impact_value}.csv",
            index=False)
