import textwrap
import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown
from src.components.toggle import create_toggle
from src.components.radio_items import create_radio_items
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

new_constr_toggle_yaml = config.get('new_constr_toggle_cat')
assert new_constr_toggle_yaml is not None, 'The config for new construction could not be set'

outlier_toggle_yaml = config.get('outlier_toggle_cat')
assert outlier_toggle_yaml is not None, 'The config for outlier toggle could not be set'

floor_area_radio_yaml = config.get('floor_area_normalization_cat')
assert floor_area_radio_yaml is not None, 'The config for floor area norm. could not be set'

sort_box_radio_yaml = config.get('sort_box_plot_cat')
assert sort_box_radio_yaml is not None, 'The config for box plot sorting could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

category_order_map = config.get('category_order_map')
assert category_order_map is not None, 'The config for category orders could not be set'

cfa_gfa_map = config.get('cfa_gfa_map')
assert cfa_gfa_map is not None, 'The config for cfa/gfa map could not be set'

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

sort_box_radio = create_radio_items(
    label=sort_box_radio_yaml['label'],
    radio_list=sort_box_radio_yaml['radio_list'],
    first_item=sort_box_radio_yaml['first_item'],
    radio_id=sort_box_radio_yaml['radio_id']
)

controls_cat = dbc.Card(
    [
        categorical_dropdown,
        total_impact_dropdown,
        floor_area_radio,
        sort_box_radio,
        new_constr_toggle,
        outlier_toggle
    ],
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
        Input('sort_box_plot_cat', 'value'),
        Input('floor_area_normal_cat', 'value'),
        Input('new_constr_toggle_cat', 'value'),
        Input('outlier_toggle_cat', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_chart(category_x,
                 objective,
                 sort_type,
                 cfa_gfa_type,
                 new_constr_toggle_cat,
                 outlier_toggle_cat,
                 buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    if new_constr_toggle_cat == [1]:
        df = df[df['bldg_proj_type'] == 'New Construction']
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
    cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
    # cfa_gfa_name_for_annotation = cfa_gfa_mapping.get('name')
    objective_for_graph = cfa_gfa_mapping.get(objective)
    
    if outlier_toggle_cat == [1]:
        Q1 = df[objective_for_graph].quantile(0.25)
        Q3 = df[objective_for_graph].quantile(0.75)
        IQR = Q3 - Q1
        df = df[
            (df[objective_for_graph] < Q3 + 3 * IQR)
            & (df[objective_for_graph] > Q1 - 3 * IQR)
        ]

    if sort_type == 'median':
        grouped_medians = (
            df[[category_x, objective_for_graph]]
            .groupby(by=category_x)
            .median()
            .sort_values(
                by=objective_for_graph,
                ascending=False
            )
        )
        category_order = grouped_medians.index.to_list()
    else:
        category_order = category_order_map.get(category_x)

    max_of_df = df[objective_for_graph].max()
    xshift = create_graph_xshift(max_value=max_of_df)

    def customwrap(s, width=25):
        if s is not None:
            return "<br>".join(textwrap.wrap(s, width=width))
    
    df[category_x] = df[category_x].map(customwrap)
    wrapped_category_order = [customwrap(s) for s in category_order]

    fig = px.box(
        data_frame=df,
        y=category_x,
        x=objective_for_graph,
        category_orders={
            category_x: wrapped_category_order
        },
        color_discrete_sequence=["#ffc700"],
        height=500
    )
    for s in df[category_x].unique():
        if len(df[df[category_x] == s]) > 0:
            fig.add_annotation(
                y=str(s),
                x=max_of_df+xshift,
                text=f'n={str(len(df[df[category_x]==s][category_x]))}',
                showarrow=False
            )

    if objective in ['epi', 'api', 'sfpi']:
        tickformat_decimal =',.2f'
    elif objective == 'odpi':
        tickformat_decimal =',.6f'
    else:
        tickformat_decimal =',.0f'     

    fig.update_xaxes(
        title=field_name_map.get(objective_for_graph) + f' {units_map.get(objective)}',
        range=[0, max_of_df+xshift],
        tickformat=tickformat_decimal,
        )
    fig.update_yaxes(
        title=field_name_map.get(category_x),
        tickformat=tickformat_decimal,
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
        Input('floor_area_normal_cat', 'value'),
        Input('new_constr_toggle_cat', 'value'),
        Input('outlier_toggle_cat', 'value'),
        State('buildings_metadata', 'data')
    ]
)
def update_table(cat_value,
                 impact_value,
                 cfa_gfa_type,
                 new_constr_toggle_cat,
                 outlier_toggle_cat,
                 buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
    df[cat_value] = df[cat_value].fillna('NULL')
    if new_constr_toggle_cat == [1]:
        df = df[df['bldg_proj_type'] == 'New Construction']

    cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
    impact_value_for_graph = cfa_gfa_mapping.get(impact_value)
    
    if outlier_toggle_cat == [1]:
        Q1 = df[impact_value_for_graph].quantile(0.25)
        Q3 = df[impact_value_for_graph].quantile(0.75)
        IQR = Q3 - Q1
        df = df[
            (df[impact_value_for_graph] < Q3 + 3 * IQR)
            & (df[impact_value_for_graph] > Q1 - 3 * IQR)
        ]

    tbl_df = (
        df.groupby(
            cat_value, as_index=False
        )[impact_value_for_graph]
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

    if impact_value in ['epi', 'api', 'sfpi']:
        valueformatter = {"function": "d3.format(',.2f')(params.value)"}
    elif impact_value == 'odpi':
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
        State('floor_area_normal_cat', 'value'),
        State('categorical_dropdown', 'value'),
        State('total_impact_dropdown', 'value'),
        State('new_constr_toggle_cat', 'value'),
        State('outlier_toggle_cat', 'value'),
        State('buildings_metadata', 'data')
    ],
    prevent_initial_call=True,
)
def func(n_clicks,
         cfa_gfa_type,
         cat_value,
         impact_value,
         new_constr_toggle_cat,
         outlier_toggle_cat,
         buildings_metadata):
    if n_clicks > 0:
        df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))
        df[cat_value] = df[cat_value].fillna('NULL')
        if new_constr_toggle_cat == [1]:
            df = df[df['bldg_proj_type'] == 'New Construction']

        cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
        impact_value_for_graph = cfa_gfa_mapping.get(impact_value)
        
        if outlier_toggle_cat == [1]:
            Q1 = df[impact_value_for_graph].quantile(0.25)
            Q3 = df[impact_value_for_graph].quantile(0.75)
            IQR = Q3 - Q1
            df = df[
                (df[impact_value_for_graph] < Q3 + 3 * IQR)
                & (df[impact_value_for_graph] > Q1 - 3 * IQR)
            ]

        tbl_df = (
            df.groupby(
                cat_value, as_index=False
            )[impact_value_for_graph]
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

        return dcc.send_data_frame(
            tbl_df.to_csv,
            f"{cat_value} values by {impact_value_for_graph}.csv",
            index=False
        )
