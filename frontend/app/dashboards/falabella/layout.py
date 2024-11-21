from dash import html, dcc, dash_table

def create_layout():
    return html.Div([
        # Contenedor para estado vacío
        html.Div(
            id='empty-state-container',
            style={'display': 'none'},
            children=html.Div([
                html.H3(
                    "Actualmente no hay información disponible para mostrar",
                    style={
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#111827',
                        'marginBottom': '16px',
                        'textAlign': 'center'
                    }
                ),
                html.P([
                    "Si no has cargado documento aún, ",
                    html.A(
                        "ve a la sección de documentos",
                        href="/dashboard/my-account/documents/",
                        style={
                            'color': '#2563EB',
                            'textDecoration': 'underline',
                            'hover': {'color': '#1E40AF'}
                        }
                    ),
                    " y carga tus estados de cuenta."
                ], style={
                    'textAlign': 'center',
                    'marginBottom': '24px',
                    'color': '#4B5563'
                }),
                html.A(
                    "Ir a Documentos",
                    href="/dashboard/my-account/documents/",
                    style={
                        'backgroundColor': '#2563EB',
                        'color': 'white',
                        'padding': '12px 32px',
                        'borderRadius': '6px',
                        'textDecoration': 'none',
                        'hover': {'backgroundColor': '#1E40AF'},
                        'display': 'inline-block'
                    }
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '48px 16px',
                'maxWidth': '600px',
                'margin': '0 auto'
            })
        ),
        
        # Contenedor principal del dashboard
        html.Div([
            html.Div([
                html.Div([
                    html.H3(id="periodo-facturacion-falabella", className="periodo-title"),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div("Pago total", className="card-title"),
                                html.Div(id="pago-total-mes-falabella", className="card-value"),
                                html.Div(id="pago-total-comparison-falabella", className="card-comparison"),
                            ], className="card"),
                            html.Div([
                                html.Div("Pago mínimo", className="card-title"),
                                html.Div(id="pago-minimo-mes-falabella", className="card-value"),
                                html.Div(id="pago-minimo-comparison-falabella", className="card-comparison"),
                            ], className="card"),
                        ], className="card-row"),
                        html.Div([
                            html.Div([
                                html.Div("Fecha máxima de pago", className="card-title"),
                                html.Div(id="fecha-maxima-pago-falabella", className="card-value"),
                            ], className="card"),
                            html.Div([
                                html.Div("Línea disponible", className="card-title"),
                                html.Div(id="linea-disponible-falabella", className="card-value"),
                            ], className="card"),
                        ], className="card-row"),
                    ], className="cards-container"),
                ], className="periodo-section"),
                html.Div([
                    html.H4("Histórico de facturación por periodo", className="chart-title"),
                    dcc.Graph(
                        id='consumption-graph-falabella',
                        className="chart-content",
                        config={'displayModeBar': False, 'responsive': True}
                    ),
                ], className="chart-container"),
            ], className="top-section"),
            html.Div([
                html.H4("Movimientos del último periodo", className="table-title"),
                dash_table.DataTable(
                    id='movimientos-table-falabella',
                    columns=[
                        {"name": "Fecha de transacción", "id": "fecha_transaccion"},
                        {"name": "Detalle", "id": "detalle"},
                        {"name": "Monto (S/)", "id": "monto"},
                        {"name": "Cuota Cargada", "id": "cuota_cargada"},
                        {"name": "% TEA", "id": "porcentaje_tea"},
                        {"name": "Capital (S/)", "id": "capital"},
                        {"name": "Interés (S/)", "id": "interes"},
                        {"name": "Total (S/)", "id": "total"}
                    ],
                    data=[],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'font-family': 'Montserrat, sans-serif',
                        'textAlign': 'left',
                        'padding': '12px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_header={
                        'backgroundColor': '#007bff',
                        'color': 'white',
                        'fontWeight': '600',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        },
                        {
                            'if': {'column_id': ['monto', 'cuota_cargada', 'porcentaje_tea', 'capital', 'interes', 'total']},
                            'textAlign': 'right'
                        }
                    ],
                ),
            ], className="table-container")
        ], id='dashboard-content', className="container")
    ])