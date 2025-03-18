from dash import html
import dash_bootstrap_components as dbc


def create_header() -> html.Div:
    """_summary_

    Returns:
        html.Div: _description_
    """
    navbar = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(
                                src='assets/W-Logo_Purple_RGB.png',
                                height="70px",
                            ),
                            href='https://lifecyclelab.org'
                        ),
                        width=3,
                        align='center'
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            'WBLCA Benchmark Study v2 Dashboard',
                            className='fs-3 text-white fw-bolder text-wrap'
                        ),
                        width=6,
                        class_name='text-center',
                        align='center'
                    ),
                    dbc.Col(
                        dbc.Nav(
                            [
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
                                    ],
                                    nav=True,
                                    toggleClassName='fs-5 text-white fw-bolder',
                                    color='white',
                                )
                            ],
                            horizontal='end'
                        ),
                        align='center',
                        width=3
                    )
                ],
                class_name='p-2'
            ),
        ],
        fluid=True,
        class_name='bg-primary justify-content-between',
    )

    return navbar
