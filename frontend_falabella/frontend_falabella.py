from flask import Flask, render_template
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objs as go

# Configurar Flask
server = Flask(__name__)

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

# Configurar Dash dentro de Flask
app = Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP, '/static/css/styles.css', 'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap']
)

# Definir el layout de la aplicación Dash
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3(id="periodo-facturacion", className="periodo-title"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div("Pago total", className="card-title"),
                        html.Div(id="pago-total-mes", className="card-value"),
                        html.Div("0% ▲ del mes anterior", className="card-comparison"),
                    ], className="card"),
                    html.Div([
                        html.Div("Pago mínimo", className="card-title"),
                        html.Div(id="pago-minimo-mes", className="card-value"),
                        html.Div("0% ▲ del mes anterior", className="card-comparison"),
                    ], className="card"),
                ], className="card-row"),
                html.Div([
                    html.Div([
                        html.Div("Fecha máxima de pago", className="card-title"),
                        html.Div(id="fecha-maxima-pago", className="card-value"),
                    ], className="card"),
                    html.Div([
                        html.Div("Línea disponible", className="card-title"),
                        html.Div(id="linea-disponible", className="card-value"),
                    ], className="card"),
                ], className="card-row"),
            ], className="cards-container"),
        ], className="periodo-section"),
        html.Div([
            html.H4("Histórico de facturación por periodo", className="chart-title"),
            dcc.Graph(
                id='consumption-graph',
                className="chart-content",
                config={'displayModeBar': False, 'responsive': True}
            ),
        ], className="chart-container"),
    ], className="top-section"),
    html.Div([
        html.H4("Movimientos del último periodo", className="table-title"),
        dash_table.DataTable(
            id='movimientos-table',
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
                #'textTransform': 'uppercase',
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
], className="container")

# Callback para actualizar el pago total y movimientos del último periodo
@app.callback(
    [
        Output('pago-total-mes', 'children'),
        Output('pago-minimo-mes', 'children'),
        Output('fecha-maxima-pago', 'children'),
        Output('linea-disponible', 'children'),
        Output('movimientos-table', 'data'),
        Output('periodo-facturacion', 'children')
    ],
    [Input('movimientos-table', 'id')]
)
def update_latest_period(_):
    try:
        response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/latest-period-data")
        response.raise_for_status()
        data = response.json()

        pago_total_mes = f"S/ {data['pago_total_mes']:.2f}"
        pago_minimo_mes = f"S/ {data['pago_minimo_mes']:.2f}"
        fecha_maxima_pago = data['ultimo_dia_pago']
        linea_disponible = f"S/ {data['linea_disponible']:.2f}"
        ultimo_periodo = data['periodo']
        movimientos = data['movimientos']

        for mov in movimientos:
            mov['fecha_transaccion'] = pd.to_datetime(mov['fecha_transaccion']).strftime('%Y-%m-%d')
            mov['monto'] = "-" if mov['monto'] == 0.00 else f"S/ {mov['monto']:.2f}"
            mov['porcentaje_tea'] = "-" if mov['porcentaje_tea'] == 0.00 else f"{mov['porcentaje_tea']:.2f}%"
            mov['capital'] = "-" if mov['capital'] == 0.00 else f"S/ {mov['capital']:.2f}"
            mov['interes'] = "-" if mov['interes'] == 0.00 else f"S/ {mov['interes']:.2f}"
            mov['total'] = f"S/ {mov['total']:.2f}"
            mov['cuota_cargada'] = "-" if mov['cuota_cargada'] == "NA" else mov['cuota_cargada']

        periodo_facturacion = html.Span([
            "Periodo de facturación: ",
            html.Span(ultimo_periodo, style={"color": "#007bff"})
        ])

        return pago_total_mes, pago_minimo_mes, fecha_maxima_pago, linea_disponible, movimientos, periodo_facturacion

    except requests.exceptions.RequestException as e:
        return "Error", "Error", "Error", "Error", [], "Error al cargar datos"

# Callback para actualizar el gráfico de consumo por periodo
@app.callback(
    Output('consumption-graph', 'figure'),
    Input('consumption-graph', 'id')
)
def update_graph(_):
    try:
        response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/consumption-data")
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)

        figure = go.Figure(data=[
            go.Scatter(x=df['periodo'], y=df['pago_total_mes'], mode='lines+markers', line=dict(color='#007bff', width=2))
        ])

        figure.update_layout(
            xaxis_title="Periodo de Facturación",
            yaxis_title="Pago Total (S/)",
            font=dict(family="Montserrat", size=16),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=20, t=50, b=100),
            height=350,
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey',
                linecolor='black',
                tickangle=45,
                tickfont=dict(size=14),
                tickformat='%m/%y',
                nticks=6
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey',
                linecolor='black',
                tickformat=',.0f',
                nticks=5,
                tickfont=dict(size=14)
            ),
        )

        # Ajustes específicos para dispositivos móviles
        figure.update_layout(
            autosize=True,
            xaxis=dict(
                rangeselector=dict(visible=False),
                rangeslider=dict(visible=False)
            )
        )

        return figure

    except requests.exceptions.RequestException as e:
        return go.Figure()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)