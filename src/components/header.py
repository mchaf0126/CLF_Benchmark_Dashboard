from dash import html
import dash_bootstrap_components as dbc


def create_header() -> html.Div:
    """_summary_

    Returns:
        html.Div: _description_
    """
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                html.Img(
                                    src='assets/CLF_Logo_Rev_MED.png',
                                    height="70px"
                                ),
                                href='https://carbonleadershipforum.org'
                            )
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                'WBLCA Benchmark Dashboard',
                                className='fs-3 text-white fw-bolder'
                            ),
                        ),
                    ],
                    align='center',
                    justify='left',
                    className='g-4'
                ),
                dbc.Nav([
                    dbc.NavItem(
                            dbc.NavLink(
                                'Home',
                                href='/',
                                className='fs-5 text-white fw-bolder'
                            ),
                    ),
                    dbc.DropdownMenu(
                        label='Explore the data',
                        children=[
                            dbc.DropdownMenuItem(
                                "Box plot",
                                href="box_plot"
                            ),
                            dbc.DropdownMenuItem(
                                "Scatter plot",
                                href="scatter_plot"
                            ),
                            dbc.DropdownMenuItem(
                                "Stacked bar chart",
                                href="stacked_bar_chart"
                            )
                        ],
                        nav=True,
                        toggleClassName='fs-5 text-white fw-bolder',
                        color='white'
                    )
                ])
            ],
            fluid=True
        ),
        color='secondary',
    ),
    return navbar
