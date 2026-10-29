#!/usr/bin/env bash
#
# Prepara la base de datos local para la app Flask (crud_productos).
#
# Uso:
#   bash setup_db.sh
#
# Hace lo siguiente:
#   1. Crea la base de datos crud_productos.
#   2. Permite que root conecte por TCP sin contrasena (lo que usa db.py).
#   3. Crea las tablas base y ejecuta las migraciones del repositorio.
#   4. Verifica la conexion.
#
# Requiere sudo (te pedira tu contrasena).

set -euo pipefail

DB_NAME="crud_productos"
SQL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/sql"

# Ejecuta mariadb como root del sistema (socket con privilegios).
mariadb_root() {
    sudo mariadb "$@"
}

echo "==> 0/4  Verificando que MariaDB este activo..."
if ! systemctl is-active --quiet mariadb; then
    echo "ERROR: el servicio mariadb no esta corriendo." >&2
    echo "       Inicialo con: sudo systemctl enable --now mariadb" >&2
    exit 1
fi

echo "==> 1/4  Recreando base de datos '$DB_NAME' (se borra cualquier dato previo)..."
mariadb_root -e "DROP DATABASE IF EXISTS $DB_NAME;"
mariadb_root -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "==> 2/4  Habilitando conexion TCP de root sin contrasena..."
mariadb_root <<'SQL'
ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('');
CREATE USER IF NOT EXISTS 'root'@'127.0.0.1' IDENTIFIED VIA mysql_native_password USING PASSWORD('');
GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SQL

echo "==> 3/4  Creando tablas y aplicando migraciones..."
for archivo in \
    "crear_tabla_usuarios.sql" \
    "crear_tabla_productos.sql" \
    "actualizar_inventario_y_ventas.sql" \
    "compradores_ventas.sql"
do
    if [[ ! -f "$SQL_DIR/$archivo" ]]; then
        echo "ERROR: no se encontro $SQL_DIR/$archivo" >&2
        exit 1
    fi
    echo "       - $archivo"
    mariadb_root "$DB_NAME" < "$SQL_DIR/$archivo"
done

echo "==> 4/4  Verificando (conexion TCP como root, igual que db.py)..."
if command -v mariadb >/dev/null 2>&1; then
    mariadb -h 127.0.0.1 -P 3306 -u root "$DB_NAME" \
        -e "SELECT VERSION() AS version; SHOW TABLES;"
else
    mariadb_root "$DB_NAME" -e "SELECT VERSION() AS version; SHOW TABLES;"
fi

echo
echo "Listo. Base '$DB_NAME' creada con las tablas:"
echo "  usuarios, productos, ventas, compradores"
