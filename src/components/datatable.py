from dash import dash_table, html
from dash.dash_table.Format import Format, Scheme


def create_datatable(table_id: str) -> html.Div:
    """_summary_

    Returns:
        html.Div: _description_
    """
    return html.Div(
        dash_table.DataTable(
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={
                'textAlign': 'left',
                'minWidth': '150 px',
                'width': '150px',
                'maxWidth': '150px'
            },
            page_size=8,
            style_data={
                'border': 'none',
                'height': 'auto',
                'whiteSpace': 'normal'
            },
            style_header={
                'textAlign': 'left',
                'fontWeight': 'bold',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            id=table_id,
        ),
        className='dbc'
    )


def create_string_table_entry(column_name: str) -> dict:
    """_summary_

    Args:
        column_name (str): _description_

    Returns:
        dict: _description_
    """
    return {
        'id': column_name,
        'name': column_name,
        'type': 'numeric',
        'format': Format(precision=2, scheme=Scheme.fixed)
    }


def create_float_table_entry(column_name: str) -> dict:
    """_summary_

    Args:
        column_name (str): _description_

    Returns:
        dict: _description_
    """
    return {
        'id': column_name,
        'name': column_name,
        'type': 'numeric',
        'format': Format(precision=2, scheme=Scheme.fixed)
    }


def create_int_table_entry(column_name: str) -> dict:
    """_summary_

    Args:
        column_name (str): _description_

    Returns:
        dict: _description_
    """
    return {
        'id': column_name,
        'name': column_name,
        'type': 'numeric',
        'format': Format(precision=2, scheme=Scheme.decimal_integer)
    }
