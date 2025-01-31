from dash import html, dcc
import dash_bootstrap_components as dbc


def create_dropdown(label: str, dropdown_list: list, first_item: str, dropdown_id: str) -> html.Div:
    """_summary_

    Args:
        labe (str): _description_
        dropdown_list (list): _description_
        first_item (str): _description_
        id (str): _description_

    Returns:
        html.Div: _description_
    """

    dropdown = html.Div(
        [
            dbc.Label(label),
            dcc.Dropdown(
                options=dropdown_list,
                value=first_item,
                id=dropdown_id,
                clearable=False,
                optionHeight=60
            ),
        ],
        className='mb-4'
    )
    return dropdown
