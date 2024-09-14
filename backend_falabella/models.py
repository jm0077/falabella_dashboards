from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class InfoGeneral(Base):
    __tablename__ = 'info_general'
    id = Column(Integer, primary_key=True)
    userId = Column(String(36), index=True)  # Add index here
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

class Movimiento(Base):
    __tablename__ = 'info_movimientos'
    id = Column(Integer, primary_key=True)
    userId = Column(String(36), index=True)  # Add index here
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

# Create an index on userId for both tables
Index('idx_info_general_userId', InfoGeneral.userId)
Index('idx_movimiento_userId', Movimiento.userId)