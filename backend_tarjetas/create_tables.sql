CREATE TABLE IF NOT EXISTS banco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario_banco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId VARCHAR(36),
    banco_id INT,
    habilitado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (banco_id) REFERENCES banco(id)
);

CREATE TABLE IF NOT EXISTS usuario_estado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId VARCHAR(36),
    primer_ingreso BOOLEAN DEFAULT TRUE,
    documento_cargado BOOLEAN DEFAULT FALSE,
    fecha_primer_ingreso TIMESTAMP,
    fecha_primera_carga TIMESTAMP,
    UNIQUE KEY uk_usuario_estado_userId (userId)
);