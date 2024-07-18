from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from src.components.header import create_header
from src.components.footer import create_footer

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

load_figure_template('clf')

header = create_header()
footer = create_footer()


app.layout = dbc.Container(
    [
        html.Div(
            children=[
                dbc.Row(
                    html.Header(
                        dbc.Row(
                            dbc.Col(
                                header,
                                className='mb-2',
                                width={'size': 10}
                            ),
                            justify='center'
                        ),
                    )
                ),
                dbc.Row(
                    page_container
                ),
                dbc.Row(
                    html.Footer(
                        dbc.Row(
                            dbc.Col(
                                footer,
                                className='mt-2',
                                width={'size': 10}
                            ),
                            justify='center'
                        ),
                    )
                )
            ],
        ),
    ],
    fluid=True,
    className='dbc'
)


if __name__ == "__main__":
    app.run_server(debug=True)
