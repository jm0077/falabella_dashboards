from flask import Flask, render_template
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd

# Configurar Flask
server = Flask(__name__)

# Configurar Dash dentro de Flask
app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir el layout de la aplicación Dash
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard de Consumo Mensual"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='consumption-graph'), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Pago Total del Último Mes"), className="text-center"),
        dbc.Col(html.H1(id='latest-payment', className="text-center text-success"), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H3("Movimientos del Último Mes"), className="text-center"),
        dbc.Col(dash_table.DataTable(id='latest-movements'), width=12),
    ])
], fluid=True)

# Callback para actualizar el gráfico de consumo mensual
@app.callback(
    Output('consumption-graph', 'figure'),
    Input('consumption-graph', 'id')
)
def update_consumption_graph(_):
    # Realizar solicitud al backend
    response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/consumption-data")
    data = response.json()

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear la figura del gráfico de líneas
    fig = {
        'data': [
            {'x': df['mes'], 'y': df['monto_consumido'], 'type': 'line', 'name': 'Monto Consumido'},
            {'x': df['mes'], 'y': df['monto_en_cuotas'], 'type': 'line', 'name': 'Monto en Cuotas'},
            {'x': df['mes'], 'y': df['pago_total_mes'], 'type': 'line', 'name': 'Pago Total Mes'},
        ],
        'layout': {
            'title': 'Consumo Mensual',
            'xaxis': {'title': 'Mes'},
            'yaxis': {'title': 'Monto'},
        }
    }
    return fig

# Callback para actualizar la información del último mes
@app.callback(
    [Output('latest-payment', 'children'), Output('latest-movements', 'data'), Output('latest-movements', 'columns')],
    Input('latest-payment', 'id')
)
def update_latest_month_data(_):
    # Realizar solicitud al backend
    response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/latest-month-data")
    data = response.json()

    # Obtener pago total mes
    latest_payment = f"S/ {data['pago_total_mes']:.2f}"

    # Preparar datos para la tabla
    movements = pd.DataFrame(data['movimientos'])

    columns = [{"name": i, "id": i} for i in movements.columns]

    return latest_payment, movements.to_dict('records'), columns

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8050)
