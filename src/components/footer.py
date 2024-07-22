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

                            html.A(
                                html.Img(src='assets/github.png', height='40px'),
                                href='https://github.com/mchaf0126/CLF_Benchmark_Dashboard',
                                className='mx-2'
                            ),
                            html.A(
                                html.Img(src='assets/linkedin.png', height='40px'),
                                href='https://www.linkedin.com/company/carbon-leadership-forum/',
                                className='mx-2'
                            ),
                            html.A(
                                html.Img(src='assets/youtube.png', height='35px'),
                                href='https://www.youtube.com/channel/UCPeIwsmA8ul3iazdy5M9i2w',
                                className='mx-2'
                            ),
                        ],
                        width={'size': 4},
                        class_name='text-center'
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
                justify='end',
                align='center'
            )
        ],
        fluid=True,
        class_name='bg-body-secondary p-3 fs-6'
    )

    return navbar
