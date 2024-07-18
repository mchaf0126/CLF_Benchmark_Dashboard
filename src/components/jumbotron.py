from dash import html
import dash_bootstrap_components as dbc


def create_jumbotron(main_text: str, subtitle: list) -> html.Div:
    """_summary_

    Args:
        main_text (str): _description_
        subtitle (list): _description_

    Returns:
        html.Div: _description_
    """

    jumbotron = html.Div(
        dbc.Container(
            [
                html.H1(main_text, className="my-2"),
                html.P(
                    subtitle,
                    className="lead fs-5 my-2",
                ),
                html.Hr(className="mb-2"),
            ],
            fluid=True,
            className="text-center py-1",
        ),
        className="mb-5 p-0 bg-body-secondary rounded-3",
    )
    return jumbotron
