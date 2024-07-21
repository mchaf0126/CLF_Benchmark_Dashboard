from pathlib import Path
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
from src.components.jumbotron import create_jumbotron


register_page(__name__, path='/')

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
data_directory = main_directory.joinpath('data/public_dataset_fake_07-10-2024.csv')

typology_jumbotron = create_jumbotron(
    main_text='17',
    subtitle='Unique Building Typologies'
)

project_number_jumbotron = create_jumbotron(
    main_text='275',
    subtitle='New Construction Projects'
)

avg_impact_jumbotron = create_jumbotron(
    main_text='560',
    subtitle='Average kg CO2 / m2'
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
                            currently three types of graphs available, with
                            more to come in the future:
                            *  **Box plot** - the traditional benchmarking graph.
                            This plot will show evironmental impacts based on
                            categorical variables
                            *  **Scatter plot** - good for analyzing relationships.
                            This plot will show evironmental impacts compared
                            to continuous variables.
                            *  **Stacked bar chart** - a way to compare average impacts.
                            This chart will show the _average_ impacts of a categorical
                            variable split across either life cycle stage or building
                            element (as described by OmniClass).
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
