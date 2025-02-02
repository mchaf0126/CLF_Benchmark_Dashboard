import plotly.express as px
from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from src.components.dropdowns import create_dropdown
from src.utils.load_config import app_config

register_page(__name__, path='/parallel_coordinates')

load_figure_template('clf')

config = app_config

parallel_coord_yaml = config.get('parallel_coord_checklist')
assert parallel_coord_yaml is not None, 'The config for cont. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

checklist = html.Div(
    [
        dbc.Label(parallel_coord_yaml.get('label')),
        dbc.Checklist(
            options=parallel_coord_yaml.get('options'),
            value=parallel_coord_yaml.get('value'),
            id=parallel_coord_yaml.get('id'),
            inputCheckedClassName="border border-primary bg-primary"
        )
    ],
)

total_impact_dropdown = create_dropdown(
    label=total_impact_dropdown_yaml['label'],
    dropdown_list=total_impact_dropdown_yaml['dropdown_list'],
    first_item=total_impact_dropdown_yaml['first_item'],
    dropdown_id=total_impact_dropdown_yaml['dropdown_id']
)

controls_cont = dbc.Card(
    [
        html.Div(
            checklist,
        ),
        html.Div(
            total_impact_dropdown,
            className='my-3'
        )
    ],
    body=True,
)


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
                        dcc.Graph(id='parallel_coord'),
                    ], xs=7, sm=7, md=8, lg=8, xl=8, xxl=8
                ),
            ],
            justify='center',
            className='mb-4'
        ),
    ],
)


@callback(
    Output('parallel_coord', 'figure'),
    Input('parallel_coord_checklist', 'value'),
    Input('total_impact_dropdown', 'value')
)
def update_chart(dimensions, impact_value):
    dimensions = sorted(dimensions, key=parallel_coord_yaml.get('order').index)
    dimensions.append(impact_value)
    fig = px.parallel_coordinates(
        df,
        dimensions=dimensions,
        color=impact_value,
        template='clf',
    )
    return fig
