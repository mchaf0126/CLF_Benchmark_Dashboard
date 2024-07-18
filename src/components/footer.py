from dash import html
import dash_bootstrap_components as dbc


def create_footer() -> html.Div:
    """_summary_

    Returns:
        html.Div: _description_
    """
    navbar = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(''),
                        width={'size': 4}
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.A(
                                        'Website  |',
                                        href='https://carbonleadershipforum.org/clf-wblca-v2/',
                                    ),
                                    html.A(
                                        '  Github  |',
                                        href='https://github.com/mchaf0126/CLF_Benchmark_Dashboard',
                                    ),
                                    html.A(
                                        ' California Carbon Report',
                                        href='https://carbonleadershipforum.org/california-carbon/',
                                    ),
                                ],                                
                                className='text-center fw-bold'
                            )
                        ],
                        width={'size': 4}
                    ),
                    dbc.Col(
                        html.Div(
                            html.Small(
                                '© Copyright 2024, Carbon Leadership Forum'
                                ), 
                            className='text-end fw-light',
                        ),
                        width={'size': 4}
                    )
                ],
                justify='end'
            )
        ],
        fluid=True,
        class_name='bg-body-secondary p-3 fs-6'
    )

    return navbar
