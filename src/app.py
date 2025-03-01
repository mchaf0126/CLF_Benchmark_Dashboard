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
)
current_file_path = Path(__file__)
main_directory = current_file_path.parents[1]
data_directory = main_directory.joinpath('data/buildings_metadata_fake_01-30-2025.xlsx')

buildings_metadata_df = pd.read_excel(data_directory, index_col=False)

load_figure_template('clf')

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
                        width={'size': 10}
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
