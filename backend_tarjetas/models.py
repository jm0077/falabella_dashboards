from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey, Index, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Banco(Base):
    __tablename__ = 'banco'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)

class UsuarioBanco(Base):
    __tablename__ = 'usuario_banco'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String(36), index=True)
    banco_id = Column(Integer, ForeignKey('banco.id'), nullable=False)
    habilitado = Column(Boolean, default=False)
    
    banco = relationship('Banco', backref='usuario_bancos')

# Create indices
Index('idx_usuario_banco_userId', UsuarioBanco.userId)
Index('idx_banco_id', UsuarioBanco.banco_id)