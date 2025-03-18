from pathlib import Path
import pandas as pd
from dash import Dash, html, page_container, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from src.components.header import create_header

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.PULSE]
)
server = app.server
current_file_path = Path(__file__)
main_directory = current_file_path.parents[1]
data_directory = main_directory.joinpath('data/buildings_metadata.xlsx')

buildings_metadata_df = pd.read_excel(data_directory, index_col=False)

load_figure_template('pulse')

header = create_header()

app.layout = dbc.Container(
    [
        dcc.Store(
            data={
                'buildings_metadata': buildings_metadata_df.to_dict()
            },
            id='buildings_metadata',
            storage_type='memory',
        ),
        dbc.Row(
            html.Header(
                dbc.Row(
                    dbc.Col(
                        header,
                        className='mb-2',
                        xs=12, sm=12, md=12, lg=12, xl=10, xxl=10
                    ),
                    justify='center'
                ),
            )
        ),
        dbc.Row(
            page_container
        )
    ],
    fluid=True,
    className='dbc'
)


if __name__ == "__main__":
    app.run_server(debug=True)
