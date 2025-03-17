import pandas as pd
from dash import html, dcc, register_page, Input, Output, callback
import dash_bootstrap_components as dbc
from src.components.jumbotron import create_jumbotron


register_page(__name__, path='/')

typology_jumbotron = create_jumbotron(
    subtitle='Unique Building Typologies',
    main_text_id='typology_jumbotron'
)

project_number_jumbotron = create_jumbotron(
    subtitle='New Construction Projects',
    main_text_id='project_number_jumbotron'
)

avg_impact_jumbotron = create_jumbotron(
    subtitle='Average kg CO2 / m2',
    main_text_id='avg_impact_jumbotron'
)

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            '''
                            #### About this study
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            In 2017, the CLF published the Embodied Carbon
                            Benchmark Study for North American buildings.
                            Since then, the practice of whole-building life
                            cycle assessment (WBLCA) has grown rapidly in the
                            AEC industry, and it has become clear that more
                            robust and reliable benchmarks are critical for
                            advancing work in this field. This project will
                            fill a critical gap in the AEC industry and help
                            enable architects, engineers, policy makers, and
                            the entire design community to work towards
                            realistic and measurable embodied carbon reductions
                            at the building scale.
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### About the dashboard
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            At present, the dashboard is in beta. There are
                            currently four types of graphs available, with
                            more to come in the future:
                            *  **Box plot** - the traditional benchmarking graph.
                            This plot will show evironmental impacts based on
                            categorical variables
                            *  **Scatter plot** - good for analyzing relationships.
                            This plot will show evironmental impacts compared
                            to continuous variables.
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### Useful Links
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            - **[Study Landing Page]
                            (https://carbonleadershipforum.org/clf-wblca-v2/)**
                            - **[California Carbon Report]
                            (https://carbonleadershipforum.org/california-carbon/)**
                            - **[Data Collection User Guide]
                            (https://hdl.handle.net/1773/51285)**
                            - **[Data Entry Template]
                            (https://hdl.handle.net/1773/51286)**
                            ''',
                            className='fw-light'
                        ),
                    ],
                    width={"size": 8},
                    class_name='pe-5'
                ),
                dbc.Col(
                    [
                        typology_jumbotron, project_number_jumbotron, avg_impact_jumbotron
                    ],
                    className='my-4',
                    width={'size': 2}
                ),
            ],
            justify='center',
            className='m-2'
        ),
    ]
)


@callback(
    [
        Output('typology_jumbotron', 'children'),
        Output('project_number_jumbotron', 'children'),
        Output('avg_impact_jumbotron', 'children'),
    ],
    Input('buildings_metadata', 'data')
)
def update_chart(buildings_metadata):
    df = pd.DataFrame.from_dict(buildings_metadata.get('buildings_metadata'))

    typology_jumbotron_main_text = len(df['bldg_prim_use'].unique())
    project_number_jumbotron_main_text = df.shape[0]
    avg_impact_jumbotron_main_text = round(df['eci_a_to_c_gfa'].mean())

    return typology_jumbotron_main_text, project_number_jumbotron_main_text, \
        avg_impact_jumbotron_main_text

# *  **Stacked bar chart** - a way to compare average impacts.
# This chart will show the _average_ impacts of a categorical
# variable split across either life cycle stage or building
# element (as described by OmniClass).
# *  **Parallel coordinates chart** - a way to compare different
# continuous variables and impacts. This chart will show each
# building's categorical values along with their impacts. This will
# allow the user to select different values and see how their building
# will compare against others.
