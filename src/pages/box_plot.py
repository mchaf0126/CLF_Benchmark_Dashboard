import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown
from src.components.datatable import create_datatable, \
    create_float_table_entry, create_string_table_entry
from src.utils.load_config import app_config

config = app_config

register_page(__name__, path='/box_plot')

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
                    dbc.Button(
                        "Download Table Contents",
                        color='secondary',
                        id="btn-download-tbl-box",
                        active=True,
                        className='my-2 fw-bold'
                    ),
                    dcc.Download(id="download-tbl-box"),
                    table,
                ]),
                xs=10, sm=10, md=10, lg=10, xl=8, xxl=8
            ),
            justify='center'
        )
    ],
)


@callback(
    Output('box_plot_table_data', 'data'),
    [
        Input('categorical_dropdown', 'value'),
        Input('total_impact_dropdown', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_box_plot_table_data(cat_value, impact_value, buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))

    # filter out projects with more than 5 projects
    df = df.groupby(cat_value).filter(lambda x: len(x) > 4)

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
    return {
        'box_plot_table_data': tbl_df.to_dict(),
        'cat_value': cat_value,
        'impact_value': impact_value
    }


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

    # filter out projects with more than 5 projects
    df = df.groupby(category_x).filter(lambda x: len(x) > 4)

    max_of_df = df[objective].max()
    if max_of_df <= 1:
        xshift = 0.1
    elif 1 < max_of_df < 25:
        xshift = 2
    elif 25 < max_of_df < 50:
        xshift = 5
    elif 50 < max_of_df < 100:
        xshift = 10
    elif 100 < max_of_df < 1000:
        xshift = 25
    elif 1000 < max_of_df < 10000:
        xshift = 100
    elif 10000 < max_of_df < 50000:
        xshift = 1000
    elif 50000 < max_of_df < 100000:
        xshift = 5000
    else:
        xshift = 20000

    print(max_of_df)

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
                           x=max_of_df+xshift,
                           text=f'n={str(len(df[df[category_x]==s][category_x]))}',
                           showarrow=False
                           )
    fig.update_xaxes(
        title=objective + ' (kg CO2/m2)',
        range=[0, max_of_df+xshift]
        )
    fig.update_yaxes(
        title=category_x,
    )
    fig.update_traces(
        quartilemethod='inclusive'
    )
    fig.update_layout(
        margin={'pad': 10}
    )
    return fig


@callback(
    [
        Output('results_table_cat', 'columnDefs'),
        Output('results_table_cat', 'rowData'),
    ],
    Input('box_plot_table_data', 'data')
)
def update_table(box_plot_table_data):
    tbl_df = pd.DataFrame.from_dict(box_plot_table_data.get('box_plot_table_data'))
    impact_value = box_plot_table_data.get('impact_value')
    cat_value = box_plot_table_data.get('cat_value')

    float_columns = [
        'mean',
        'std',
        'max',
        'min',
        'median',
        'Q1',
        'Q3'
    ]

    if impact_value in ['epi_a_to_c', 'api_a_to_c', 'sfpi_a_to_c']:
        valueformatter = {"function": "d3.format(',.2f')(params.value)"}
    elif impact_value == 'odpi_a_to_c':
        valueformatter = {"function": "d3.format(',.5f')(params.value)"}
    else:
        valueformatter = {"function": "d3.format(',.0f')(params.value)"}

    cols = [create_string_table_entry(cat_value)] + \
        [create_float_table_entry(float_col, valueformatter) for float_col in float_columns]
    data = tbl_df.to_dict('records')
    return cols, data


@callback(
    Output("download-tbl-box", "data"),
    [
        Input("btn-download-tbl-box", "n_clicks"),
        State('box_plot_table_data', 'data')
    ],
    prevent_initial_call=True,
)
def func(n_clicks, box_plot_table_data):
    if n_clicks > 0:
        tbl_df = pd.DataFrame.from_dict(box_plot_table_data.get('box_plot_table_data'))
        impact_value = box_plot_table_data.get('impact_value')
        cat_value = box_plot_table_data.get('impact_value')

        return dcc.send_data_frame(
            tbl_df.to_csv,
            f"{cat_value} values by {impact_value}.csv",
            index=False)
