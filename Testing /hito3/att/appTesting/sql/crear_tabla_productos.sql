-- Tabla base de productos.
-- El repositorio solo incluye las migraciones (ALTER) de inventario y ventas,
-- por lo que esta tabla base se reconstruye a partir de los campos que usa app.py.
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) DEFAULT '',
    precio DECIMAL(10,2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
