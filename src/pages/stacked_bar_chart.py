from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, register_page
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
import src.utils.general as utils
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable

register_page(__name__, path='/stacked_bar_chart')

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
data_directory = main_directory.joinpath('data/public_dataset_fake_07-10-2024.csv')

df = pd.read_csv(data_directory, index_col=False)

config_path = main_directory.joinpath('src/components/config.yml')

config = utils.read_yaml(config_path)
assert config is not None, 'The config dictionary could not be set'

categorical_dropdown_yaml = config.get('categorical_dropdown')
assert categorical_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

impact_type_dropdown_yaml = config.get('impact_type_dropdown')
assert impact_type_dropdown_yaml is not None, 'The config for total impacts could not be set'

impact_cat_yaml = config.get('impact_category')
assert impact_cat_yaml is not None, 'The config for total impacts could not be set'

categorical_dropdown = create_dropdown(
    label=categorical_dropdown_yaml['label'],
    dropdown_list=categorical_dropdown_yaml['dropdown_list'],
    first_item=categorical_dropdown_yaml['first_item'],
    dropdown_id=categorical_dropdown_yaml['dropdown_id']
)

impact_type_dropdown = create_dropdown(
    label=impact_type_dropdown_yaml['label'],
    dropdown_list=impact_type_dropdown_yaml['dropdown_list'],
    first_item=impact_type_dropdown_yaml['first_item'],
    dropdown_id=impact_type_dropdown_yaml['dropdown_id']
)

controls_cont = dbc.Card(
    [categorical_dropdown, impact_type_dropdown],
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
                        dbc.Card(
                            [dcc.Graph(id="stacked_bar")],
                            className='border rounded'
                        )
                    ], xs=7, sm=7, md=8, lg=8, xl=8, xxl=8
                ),
            ],
            justify='center',
            className='mb-4'
        ),
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
    Input('categorical_dropdown', 'value'),
    Input('impact_type_dropdown', 'value'),
)
def update_chart(cat_value, impact_type):

    fig = px.histogram(
        df,
        x=cat_value,
        y=impact_cat_yaml.get(impact_type),
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
        Output('results_table_stacked_bar', 'style_cell_conditional')
    ],
    [
        Input('categorical_dropdown', 'value'),
        Input('impact_type_dropdown', 'value')
    ]
)
def update_table(cat_value, impact_value):

    cols = [
        {
            'id': cat_value,
            'name': cat_value
        },
    ]
    for c in impact_cat_yaml.get(impact_value):
        cols.append({
                'id': c,
                'name': c,
                'type': 'numeric',
                'format': Format(precision=2, scheme=Scheme.fixed)
        })
    column_list = [cat_value]
    column_list.extend(impact_cat_yaml.get(impact_value))
    data = df[column_list].sort_values(by=cat_value).to_dict('records')
    style_cc = [
        {
            'if': {'column_id': impact_cat_yaml.get(impact_value)},
            'textAlign': 'right',
            'minWidth': '70px', 'width': '70px', 'maxWidth': '70px',
        },
    ]
    return cols, data, style_cc


@callback(
    Output("download-tbl-stack", "data"),
    State('categorical_dropdown', 'value'),
    State('impact_type_dropdown', 'value'),
    Input("btn-download-tbl-stack", "n_clicks"),
    prevent_initial_call=True,
)
def func(cat_value, impact_value, n_clicks):
    if n_clicks > 0:
        column_list = [cat_value]
        column_list.extend(impact_cat_yaml.get(impact_value))
        return dcc.send_data_frame(
            df[column_list].sort_values(by=cat_value).to_csv,
            f"{cat_value} values by {impact_value}.csv",
            index=False)
