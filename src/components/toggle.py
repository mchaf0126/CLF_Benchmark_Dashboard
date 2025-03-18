from dash import html
import dash_bootstrap_components as dbc


def create_toggle(toggle_list: list, first_item: str, toggle_id: str) -> html.Div:
    """_summary_

    Args:
        labe (str): _description_
        toggle_list (list): _description_
        first_item (str): _description_
        toggle_id (str): _description_

    Returns:
        html.Div: _description_
    """

    toggle = html.Div(
        [
            dbc.Checklist(
                options=toggle_list,
                value=first_item,
                id=toggle_id,
                switch=True,
            )
        ],
        className='mb-4'
    )
    return toggle
