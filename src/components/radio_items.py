from dash import html
import dash_bootstrap_components as dbc


def create_radio_items(label: str, radio_list: list, first_item: str, radio_id: str) -> html.Div:
    """_summary_

    Args:
        label (str): _description_
        radio_list (list): _description_
        first_item (str): _description_
        radio_id (str): _description_

    Returns:
        html.Div: _description_
    """

    radio_items = html.Div(
        [
            dbc.Label(label),
            dbc.RadioItems(
                options=radio_list,
                value=first_item,
                id=radio_id,
                persistence=True,
            ),
        ],
        className='mb-4'
    )
    return radio_items
