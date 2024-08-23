from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timedelta

app = Flask(__name__)

# Configura la conexión con la base de datos MySQL utilizando el conector de Cloud SQL
db_user = 'jm_07'
db_pass = '12345'
db_name = 'falabella'
cloud_sql_connection_name = 'custom-curve-431820-e9:southamerica-west1:my-mysql-instance'

# Crear la URL de conexión
db_url = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket=/cloudsql/{cloud_sql_connection_name}"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Base de clases para los modelos
Base = declarative_base()

# Modelo completo InfoGeneral
class InfoGeneral(Base):
    __tablename__ = 'info_general'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    tipo_tarjeta = Column(String(255))
    direccion = Column(Text)
    numero_tarjeta = Column(String(50))
    pago_minimo_mes = Column(Float)
    pago_total_mes = Column(Float)
    total_facturado_mes_anterior = Column(Float)
    correo_electronico = Column(String(255))
    numero_cuenta = Column(String(50))
    periodo_facturacion = Column(String(50))
    linea_credito = Column(Float)
    ultimo_dia_pago = Column(Date)
    linea_utilizada = Column(Float)
    linea_disponible = Column(Float)
    movimientos = relationship('Movimiento', backref='info_general')

# Modelo completo Movimiento
class Movimiento(Base):
    __tablename__ = 'info_movimientos'
    id = Column(Integer, primary_key=True)
    fecha_transaccion = Column(Date)
    fecha_proceso = Column(Date)
    detalle = Column(Text)
    monto = Column(Float)
    cuota_cargada = Column(String(50))
    porcentaje_tea = Column(Float)
    capital = Column(Float)
    interes = Column(Float)
    total = Column(Float)
    info_general_id = Column(Integer, ForeignKey('info_general.id'))

@app.route('/api/consumption-data', methods=['GET'])
def get_consumption_data():
    # Calcular la fecha de hace 12 meses
    twelve_months_ago = datetime.now() - timedelta(days=365)

    # Obtener los pagos totales de los últimos 12 meses de la tabla info_general
    results = session.query(
        func.date_format(InfoGeneral.ultimo_dia_pago, '%Y-%m').label('mes'),
        InfoGeneral.pago_total_mes
    ).filter(
        InfoGeneral.ultimo_dia_pago >= twelve_months_ago
    ).order_by(
        InfoGeneral.ultimo_dia_pago.asc()
    ).all()

    # Formatear respuesta
    response = [
        {
            'mes': r.mes,
            'pago_total_mes': r.pago_total_mes
        }
        for r in results
    ]
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
