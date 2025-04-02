from dash import html, dcc
import dash_bootstrap_components as dbc


def create_tooltip(tooltip_text: str,
                   target_id: str,
                   placement: str='top') -> html.Div:
    """Creates a tooltip for a given target.

    Args:
        tooltip_text (str): _description_
        target_id (str): _description_
        placement (str, optional): _description_. Defaults to 'top'.

    Returns:
        dbc.Tooltip: _description_
    """
    return html.Div(
        dbc.Tooltip(
            children=tooltip_text,
            target=target_id,
            placement=placement
        )
     )