from pathlib import Path
from dash import html, register_page
import dash_bootstrap_components as dbc
from src.components.jumbotron import create_jumbotron


register_page(__name__, path='/')

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
data_directory = main_directory.joinpath('data/public_dataset_fake_07-10-2024.csv')

firm_jumbotron = create_jumbotron(
    main_text='30',
    subtitle='Firms Contributing Data'
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
                    html.Div(
                        [
                            html.H3(
                                'Welcome to the CLF WBLCA Benchmark Study Dashboard!'
                            ),
                            html.Br(),
                            html.H4(
                                'About this study'
                            ),
                            html.P(
                                'In 2017, the CLF published the Embodied Carbon Benchmark Study for North American buildings. \
                                Since then, the practice of whole-building life cycle assessment (WBLCA) has grown rapidly in \
                                the AEC industry, and it has become clear that more robust and reliable benchmarks are\
                                critical for advancing work in this field. '
                            ),
                            html.Br(),
                            html.H4(
                                'Contents of the Dashboard'
                            ),
                            html.P(
                                'List of Dashboard Graphs:'
                            ),
                            html.Ul([
                                html.Li('Box plot'),
                                html.Li('Scatter plot'),
                                html.Li('Stacked bar chart')
                            ])
                        ]
                    ),
                    width={"size": 7},
                ),
                dbc.Col(
                    [
                        firm_jumbotron, project_number_jumbotron, avg_impact_jumbotron
                    ],
                    className='my-5',
                    width={'size': 2}
                ),
            ],
            justify='evenly',
            className='my-4'
        ),
    ]
)
