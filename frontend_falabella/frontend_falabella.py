from flask import Flask, render_template
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objs as go

# Configurar Flask
server = Flask(__name__)

# Configurar Dash dentro de Flask
app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir el layout de la aplicación Dash
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Pago Total del Último Periodo:", className="text-right"), width=6),
        dbc.Col(html.H2(id='pago-total-mes', className="text-left text-primary"), width=6)
    ], align='center'),  # Alineación vertical centrada
    dbc.Row([
        dbc.Col(html.H2("Movimientos del último periodo", className="text-center"), width=12),
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(id='movimientos-table', style_cell_conditional=[
            {
                'if': {'column_id': 'Total (S/)'},
                'fontWeight': 'bold',
                'color': 'red'  # Resaltar el total en negrita y con color rojo
            }
        ], style_as_list_view=True), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H2("Facturación de los últimos 12 periodos", className="text-center"))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='consumption-graph'), width=12)
    ])
], fluid=True)

# Callback para actualizar el pago total y movimientos del último periodo
@app.callback(
    [Output('pago-total-mes', 'children'),
     Output('movimientos-table', 'data'),
     Output('movimientos-table', 'columns')],
    Input('pago-total-mes', 'id')
)
def update_latest_period(_):
    # Realizar solicitud al backend
    response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/latest-period-data")
    data = response.json()

    # Pago total del último periodo
    pago_total_mes = f"S/. {data['pago_total_mes']:.2f}"

    # Movimientos del último periodo
    movimientos = data['movimientos']

    # Reordenar y etiquetar las columnas según lo solicitado
    for mov in movimientos:
        mov['fecha_transaccion'] = pd.to_datetime(mov['fecha_transaccion']).strftime('%Y-%m-%d')
        mov['fecha_proceso'] = pd.to_datetime(mov['fecha_proceso']).strftime('%Y-%m-%d')
    
    columns = [
        {"name": "Fecha de transacción", "id": "fecha_transaccion"},
        {"name": "Fecha de proceso", "id": "fecha_proceso"},
        {"name": "Detalle", "id": "detalle"},
        {"name": "Monto (S/)", "id": "monto"},
        {"name": "Cuota cargada", "id": "cuota_cargada"},
        {"name": "% TEA", "id": "porcentaje_tea"},
        {"name": "Capital (S/)", "id": "capital"},
        {"name": "Interés (S/)", "id": "interes"},
        {"name": "Total (S/)", "id": "total"}
    ]

    return pago_total_mes, movimientos, columns

# Callback para actualizar el gráfico de consumo por periodo
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
    fig = go.Figure()

    # Agregar la línea del pago total por periodo
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['pago_total_mes'],
        mode='lines+markers',
        name='Pago Total Mes',
        line=dict(color='royalblue', width=3),
        marker=dict(size=8, symbol='circle')
    ))

    # Configuración de los ejes
    fig.update_layout(
        #title='Facturación de los últimos 12 periodos',
        xaxis_title='Periodo',
        yaxis_title='Pago Total Mes (S/.)',
        xaxis=dict(showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204, 204, 204)', linewidth=2, ticks='outside'),
        yaxis=dict(showgrid=True, zeroline=True, showline=True, gridcolor='lightgrey', linecolor='rgb(204, 204, 204)', linewidth=2, tickprefix='S/.', ticksuffix=''),
        plot_bgcolor='white'
    )

    return fig

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

# Ejecutar la aplicación en el puerto 8080
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
