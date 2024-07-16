from dash import dash_table, html


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
