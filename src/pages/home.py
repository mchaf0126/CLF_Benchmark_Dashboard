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
    subtitle='Average kgCO2e / m2',
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
                            currently two types of graphs available:
                            *  **Box plot** - the traditional benchmarking graph.
                            This plot will show evironmental impacts based on
                            categorical variables. All environmental impacts are
                            inclusive of life cycle stages A-C.
                            *  **Scatter plot** - good for analyzing relationships.
                            This plot will show evironmental impacts compared
                            to continuous variables. All environmental impacts are
                            inclusive of life cycle stages A-C.
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
                            - **[Dataset hosted on Figshare]
                            (https://doi.org/10.6084/m9.figshare.28462145.v1)**
                            - **[Data Descriptor Paper (preprint)]
                            (https://doi.org/10.21203/rs.3.rs-6108016/v1)**
                            - **[Data Collection User Guide]
                            (https://hdl.handle.net/1773/51285)**
                            - **[Data Entry Template]
                            (https://hdl.handle.net/1773/51286)**
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### About the University of Washington (UW) Life Cycle Lab
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            The Life Cycle Lab at UW’s College of Built Environments leads
                            research to advance life cycle assessment (LCA) data, methods,
                            and approaches to enable the optimization of materials, buildings,
                            and infrastructure. Our work is structured to inform impactful
                            policies and practices that support global decarbonization efforts.
                            We envision a transformed, decarbonized building
                            industry – better buildings for a better planet.
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### Authors
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            The individuals from the Carbon Leadership Forum who worked on this
                            dashboard are:
                            - Brad Benke, Manager Low Carbon Buildings

                            The individuals from the UW Life Cycle Lab who worked on this
                            dashboard are:
                            - Manuel Chafart, Researcher

                            [CRediT]
                            (https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement)
                            authorship contribution: Conceptualization - B.B., M.C.,
                            Formal analysis: M.C; Methodology - B.B., M.C.;  Visualization: M.C
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### Acknowledgements
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            We would like to thank the individuals and respective firms
                            who participated in the data collection and quality assurance
                            process, this work would not have been possible without their
                            incredible support and dedication to thisproject. These
                            included: Arrowstreet Architects, Arup, BranchPattern,
                            Brightworks Sustainability, Buro Happold, BVH Architecture,
                            DCI Engineers, EHDD, Ellenzweig, Gensler, GGLO, Glumac,
                            Group 14 Engineering, Ha/f ClimateDesign, HOK, KieranTimberlake,
                            KPFF Consulting Engineers, Lake|Flato, LMN Architects,
                            Mahlum Architects, Mead & Hunt, Inc., Mithun, Perkins&Will,
                            reLoad Sustainable Design Inc., SERA Architects, Stok,
                            The Green Engineer Inc., The Miller Hull Partnership, LLP.,
                            Walter P Moore, and ZGF Architects LLP.
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            #### Citation
                            '''
                        ),
                        dcc.Markdown(
                            '''
                            Chafart, M., Benke, B. (2025). WBLCA Benchmark Study v2 Dashboard
                            (Version 1.0) \[Computer Software]. Life Cycle Lab,
                            https://benchmark-v2.lifecyclelab.org/
                            ''',
                            className='fw-light'
                        ),
                        html.Br(),
                        dcc.Markdown(
                            '''
                            **[(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0)**
                            Life Cycle Lab 2025
                            ''',
                            className='fw-light text-center'
                        ),
                    ],
                    xs=9, sm=9, md=9, lg=9, xl=8, xxl=8,
                    class_name='pe-5'
                ),
                dbc.Col(
                    [
                        typology_jumbotron, project_number_jumbotron, avg_impact_jumbotron
                    ],
                    className='my-4',
                    xs=3, sm=3, md=3, lg=3, xl=2, xxl=2,
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
