import dash_ag_grid as dag


def create_datatable(table_id: str) -> dag.AgGrid:
    """_summary_

    Returns:
        html.Div: _description_
    """
    return dag.AgGrid(
            id=table_id,
            dashGridOptions={"domLayout": "autoHeight"},
            columnSize='responsiveSizeToFit',
            columnSizeOptions={
                'defaultMinWidth': 90,
                'columnLimits': [{'key': 'pinned_column', 'minWidth': 200}],
            },
            style={'width': '100%'},
        )


def create_string_table_entry(column_name: str) -> dict:
    """_summary_

    Args:
        column_name (str): _description_

    Returns:
        dict: _description_
    """
    return {
        'field': column_name,
        'cellClass': 'fw-bold',
        'cellStyle': {
            "wordBreak": "normal"
        },
        "wrapText": True,
        "resizable": True,
        "autoHeight": True,
        'pinned': 'left',
        'colId': 'pinned_column'
    }


def create_float_table_entry(column_name: str, valueformatter: dict) -> dict:
    """_summary_

    Args:
        column_name (str): _description_

    Returns:
        dict: _description_
    """
    return {
        'field': column_name,
        'type': 'rightAligned',
        'cellClass': 'fw-light',
        'cellDataType': 'number',
        'resizeable': True,
        'valueFormatter': valueformatter,
        'cellStyle': {
            'textAlign': 'right',
        },
    }


# def create_int_table_entry(column_name: str) -> dict:
#     """_summary_

#     Args:
#         column_name (str): _description_

#     Returns:
#         dict: _description_
#     """
#     return {
#         'id': column_name,
#         'name': column_name,
#         'type': 'numeric',
#         'format': Format(precision=2, scheme=Scheme.decimal_integer)
#     }

#     impact_col_width = 115
#     table = dag.AgGrid(
#         rowData=tm_impacts_df.to_dict("records"),
#         defaultColDef={
#             "wrapHeaderText": True,
#             "autoHeaderHeight": True,
#         },
#         columnDefs=[
#             {
#                 'field': 'Life Cycle Stage',
#                 'cellClass': 'fw-bold',
#                 'cellStyle': {
#                     "wordBreak": "normal"
#                 },
#                 "wrapText": True,
#                 "resizable": True,
#                 "autoHeight": True,
#                 'width': 190,
#                 'pinned': 'left'
#             },
#             {

#             },
#             {
#                 'field': impacts_map.get('Acidification Potential'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.0f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Eutrophication Potential'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.2f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Smog Formation Potential'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.0f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Ozone Depletion Potential'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.5f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Global Warming Potential_biogenic'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.0f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Global Warming Potential_luluc'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.0f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#             {
#                 'field': impacts_map.get('Stored Biogenic Carbon'),
#                 'type': 'rightAligned',
#                 'cellClass': 'fw-light',
#                 'cellDataType': 'number',
#                 'valueFormatter': {"function": "d3.format(',.0f')(params.value)"},
#                 'cellStyle': {
#                     'textAlign': 'right'
#                 },
#                 'width': impact_col_width
#             },
#         ],
#         dashGridOptions={"domLayout": "autoHeight"},
#         style={'width': '100%'},
#     )

#     final_table = html.Div(
#         table,
#         className='my-3'
#     )
