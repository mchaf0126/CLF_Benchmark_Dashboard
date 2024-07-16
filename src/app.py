from dash import Dash, html, page_registry, page_container
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

load_figure_template('clf')


app.layout = dbc.Container([
    html.Div(
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(
                        'CLF WBLCA Benchmarking Study v2 Dashboard',
                        className="bg-primary text-black p-2 mb-2 text-center"
                    ),
                    width=11,
                ),
                justify='center'
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink(page['name'],
                                        href=page['path'],
                                        active=True,
                                        className='bg-primary text-black me-2 mb-2 fw-bold'
                                        )
                            for page in page_registry.values()
                        ],
                        pills=True,
                    ),
                    width=11
                ),
                justify='center'
            ),
        ],
    ),
    page_container
    ],
    fluid=True,
    className='dbc'
)


if __name__ == "__main__":
    app.run_server(debug=True)
