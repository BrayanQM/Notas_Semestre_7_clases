# -*- coding: utf-8 -*-
"""
Unit Tests de las 5 funciones mas criticas del sistema.

Modulo bajo prueba : /home/eynor/Documents/semestr7/Testing /hito3/att/appTesting
Funciones cubiertas:
    1. validaciones.validar_precio
    2. validaciones.validar_cantidad
    3. models.VentaRepository.registrar
    4. app.iniciar_sesion
    5. app.requiere_rol

Cada caso sigue el patron Arrange - Act - Assert y se ejecuta con:
    python -m pytest test_funciones_criticas.py -v
"""
from decimal import Decimal

import pytest
from flask import Flask, session, jsonify
from werkzeug.security import generate_password_hash

import models
from validaciones import validar_precio, validar_cantidad
import app as sistema


# =====================================================================
# 1) validar_precio
# =====================================================================
# CRITICIDAD: es la unica barrera que impide que un producto ingrese con
# un precio nulo, negativo, infinito o desmesurado. Un fallo aqui
# contamina el precio_por_unidad, el total de cada venta y los reportes
# financieros. Se probaron los valores limite (0, negativo, techo de
# 99 999 999.99) y el redondeo a 2 decimales.

def test_validar_precio_convierte_numero_y_redondea():
    # Arrange
    entrada = 10.999
    # Act
    resultado = validar_precio(entrada)
    # Assert
    assert resultado == 11.0


def test_validar_precio_acepta_string_numerico():
    # Arrange
    entrada = "1500.50"
    # Act
    resultado = validar_precio(entrada)
    # Assert
    assert resultado == 1500.50


def test_validar_precio_rechaza_cero_y_negativos():
    # Arrange
    entradas_invalidas = (0, -100, -0.01)
    # Act / Assert
    for valor in entradas_invalidas:
        with pytest.raises(ValueError):
            validar_precio(valor)


def test_validar_precio_rechaza_no_numericos_y_nulos():
    # Arrange
    entradas_invalidas = ("abc", None, float("inf"), float("nan"))
    # Act / Assert
    for valor in entradas_invalidas:
        with pytest.raises(ValueError):
            validar_precio(valor)


def test_validar_precio_respeta_el_techo_de_negocio():
    # Arrange
    valor_limite = 99999999.99
    valor_excedido = 100000000
    # Act
    resultado = validar_precio(valor_limite)
    # Assert
    assert resultado == 99999999.99
    with pytest.raises(ValueError):
        validar_precio(valor_excedido)


# =====================================================================
# 2) validar_cantidad
# =====================================================================
# CRITICIDAD: protege el inventario. Una cantidad de venta invalida
# (0, negativa, NaN o que supere el tope) permitiria vender de mas o
# dejar el stock inconsistente. Se verifica el parametro permitir_cero
# que reutiliza la funcion para cargar stock inicial.

def test_validar_cantidad_positiva_redondea_a_tres_decimales():
    # Arrange
    entrada = "0.250"
    # Act
    resultado = validar_cantidad(entrada)
    # Assert
    assert resultado == 0.25


def test_validar_cantidad_cero_permitido_para_stock():
    # Arrange
    entrada = 0
    # Act
    resultado = validar_cantidad(entrada, permitir_cero=True)
    # Assert
    assert resultado == 0.0


def test_validar_cantidad_cero_no_permitido_en_venta():
    # Arrange
    entrada = 0
    # Act / Assert
    with pytest.raises(ValueError):
        validar_cantidad(entrada)


def test_validar_cantidad_rechaza_negativos_bool_y_nulos():
    # Arrange
    entradas_invalidas = (-1, True, None)
    # Act / Assert
    for valor in entradas_invalidas:
        with pytest.raises(ValueError):
            validar_cantidad(valor)


def test_validar_cantidad_rechaza_nan_y_exceso_del_tope():
    # Arrange
    nan = float("nan")
    excedido = 1000000000
    # Act / Assert
    with pytest.raises(ValueError):
        validar_cantidad(nan)
    with pytest.raises(ValueError):
        validar_cantidad(excedido)


# =====================================================================
# 3) VentaRepository.registrar
# =====================================================================
# CRITICIDAD: es el corazon transaccional del negocio. En una sola
# operacion bloquea el comprador y el producto, valida el stock,
# descuenta inventario, calcula el total con Decimal y registra la
# venta. Un error dejaria ventas sin respaldo de stock o perdidas de
# dinero, por eso se prueba el exito y los tres caminos de rollback.

class CursorFake:
    def __init__(self, conexion):
        self.conexion = conexion
        self.resultado = None
        self.lastrowid = None

    def execute(self, consulta, parametros):
        sql = consulta.lstrip().upper()
        if sql.startswith("SELECT") and "FROM COMPRADORES" in sql:
            comprador_id = parametros[0]
            self.resultado = (
                {"id": comprador_id}
                if comprador_id in self.conexion.compradores
                else None
            )
        elif sql.startswith("SELECT") and "FROM PRODUCTOS" in sql:
            producto_id = parametros[0]
            producto = self.conexion.producto
            self.resultado = (
                dict(producto)
                if producto is not None and producto_id == producto["id"]
                else None
            )
        elif sql.startswith("UPDATE PRODUCTOS"):
            cantidad, producto_id = parametros
            assert producto_id == self.conexion.producto["id"]
            self.conexion.producto["cantidad_stock"] -= cantidad
        elif sql.startswith("INSERT INTO VENTAS"):
            self.conexion.ventas.append(parametros)
            self.lastrowid = len(self.conexion.ventas)

    def fetchone(self):
        return self.resultado

    def close(self):
        pass


class ConnectionFake:
    def __init__(self, producto, compradores=(12,)):
        self.producto = producto
        self.compradores = set(compradores)
        self.ventas = []
        self.commits = 0
        self.rollbacks = 0
        self.snapshot = None

    def cursor(self, dictionary=False):
        assert dictionary is True
        return CursorFake(self)

    def start_transaction(self):
        snapshot_producto = dict(self.producto) if self.producto else None
        self.snapshot = (snapshot_producto, list(self.ventas))

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1
        self.producto, self.ventas = self.snapshot

    def close(self):
        pass


def producto_manzana():
    return {
        "id": 7,
        "nombre": "Manzana",
        "cantidad_stock": Decimal("4.250"),
        "unidad_medida": "kg",
        "precio_por_unidad": Decimal("2.35"),
    }


def test_venta_registrar_descuenta_stock_y_calcula_total(monkeypatch):
    # Arrange
    conexion = ConnectionFake(producto_manzana())
    monkeypatch.setattr(models, "get_connection", lambda: conexion)
    # Act
    venta = models.VentaRepository().registrar(7, 3, 1.25, 12)
    # Assert
    assert venta["total"] == 2.94
    assert venta["cantidad"] == 1.25
    assert venta["comprador_id"] == 12
    assert conexion.producto["cantidad_stock"] == Decimal("3.000")
    assert len(conexion.ventas) == 1
    assert conexion.commits == 1
    assert conexion.rollbacks == 0


def test_venta_registrar_usa_redondeo_half_up_del_total(monkeypatch):
    # Arrange
    producto = producto_manzana()
    producto["precio_por_unidad"] = Decimal("1.00")
    conexion = ConnectionFake(producto)
    monkeypatch.setattr(models, "get_connection", lambda: conexion)
    # Act
    venta = models.VentaRepository().registrar(7, 3, 1.005, 12)
    # Assert
    assert venta["total"] == 1.01
    assert conexion.commits == 1


def test_venta_registrar_stock_insuficiente_hace_rollback(monkeypatch):
    # Arrange
    conexion = ConnectionFake(producto_manzana())
    monkeypatch.setattr(models, "get_connection", lambda: conexion)
    # Act / Assert
    with pytest.raises(models.StockInsuficiente):
        models.VentaRepository().registrar(7, 3, 5, 12)
    assert conexion.producto["cantidad_stock"] == Decimal("4.250")
    assert conexion.ventas == []
    assert conexion.commits == 0
    assert conexion.rollbacks == 1


def test_venta_registrar_producto_inexistente_hace_rollback(monkeypatch):
    # Arrange
    conexion = ConnectionFake(producto=None)
    monkeypatch.setattr(models, "get_connection", lambda: conexion)
    # Act / Assert
    with pytest.raises(models.ProductoNoEncontrado):
        models.VentaRepository().registrar(999, 3, 1, 12)
    assert conexion.commits == 0
    assert conexion.rollbacks == 1


def test_venta_registrar_comprador_inexistente_hace_rollback(monkeypatch):
    # Arrange
    conexion = ConnectionFake(producto_manzana(), compradores=())
    monkeypatch.setattr(models, "get_connection", lambda: conexion)
    # Act / Assert
    with pytest.raises(models.CompradorNoEncontrado):
        models.VentaRepository().registrar(7, 3, 1, 999)
    assert conexion.ventas == []
    assert conexion.commits == 0
    assert conexion.rollbacks == 1


# =====================================================================
# 4) app.iniciar_sesion
# =====================================================================
# CRITICIDAD: es la puerta de entrada al sistema. Verifica credenciales,
# que la cuenta este activa y el hash de la contrasena antes de crear la
# sesion. Un fallo permitiria acceso anonimo o suplantacion de otro rol.

class UsuariosFake:
    def __init__(self):
        self.usuarios = {
            "admin@test.local": {
                "id": 1,
                "nombre": "Admin",
                "correo": "admin@test.local",
                "password_hash": generate_password_hash("clave1234"),
                "rol": "admin",
                "activo": True,
            },
            "inactivo@test.local": {
                "id": 2,
                "nombre": "Bloqueado",
                "correo": "inactivo@test.local",
                "password_hash": generate_password_hash("clave1234"),
                "rol": "vendedor",
                "activo": False,
            },
        }

    def buscar_por_correo(self, correo):
        return self.usuarios.get(correo)


@pytest.fixture
def cliente_sesion(monkeypatch):
    monkeypatch.setattr(sistema, "usuarios", UsuariosFake())
    return sistema.app.test_client()


def test_iniciar_sesion_valido_crea_sesion(cliente_sesion):
    # Arrange
    credenciales = {"correo": "admin@test.local", "contrasena": "clave1234"}
    # Act
    respuesta = cliente_sesion.post("/api/sesion", json=credenciales)
    # Assert
    assert respuesta.status_code == 200
    assert respuesta.json["perfil"] == "Gerente"
    assert cliente_sesion.get("/api/sesion").status_code == 200


def test_iniciar_sesion_normaliza_correo(cliente_sesion):
    # Arrange
    credenciales = {"correo": "  ADMIN@Test.Local  ", "contrasena": "clave1234"}
    # Act
    respuesta = cliente_sesion.post("/api/sesion", json=credenciales)
    # Assert
    assert respuesta.status_code == 200
    assert respuesta.json["rol"] == "admin"


def test_iniciar_sesion_correo_o_contrasena_incorrectos(cliente_sesion):
    # Arrange
    inexistente = {"correo": "nadie@test.local", "contrasena": "clave1234"}
    mala_clave = {"correo": "admin@test.local", "contrasena": "incorrecta"}
    # Act / Assert
    assert cliente_sesion.post("/api/sesion", json=inexistente).status_code == 401
    assert cliente_sesion.post("/api/sesion", json=mala_clave).status_code == 401


def test_iniciar_sesion_usuario_inactivo_es_rechazado(cliente_sesion):
    # Arrange
    credenciales = {"correo": "inactivo@test.local", "contrasena": "clave1234"}
    # Act
    respuesta = cliente_sesion.post("/api/sesion", json=credenciales)
    # Assert
    assert respuesta.status_code == 401


def test_iniciar_sesion_campos_no_texto_devuelve_400(cliente_sesion):
    # Arrange
    credenciales = {"correo": "admin@test.local", "contrasena": 12345678}
    # Act
    respuesta = cliente_sesion.post("/api/sesion", json=credenciales)
    # Assert
    assert respuesta.status_code == 400


# =====================================================================
# 5) app.requiere_rol
# =====================================================================
# CRITICIDAD: es el control de autorizacion del servidor. Envuelve cada
# endpoint protegido y decide si el usuario puede ejecutar la operacion.
# Un fallo aqui abriria escalada de privilegios (p. ej. un vendedor
# eliminando productos o creando usuarios).

def app_con_permisos():
    aplicacion = Flask(__name__)
    aplicacion.secret_key = "test-secreto"

    @aplicacion.route("/solo-admin")
    @sistema.requiere_rol("admin")
    def solo_admin():
        return jsonify({"ok": True})

    @aplicacion.route("/admin-o-vendedor")
    @sistema.requiere_rol("admin", "vendedor")
    def admin_o_vendedor():
        return jsonify({"ok": True})

    @aplicacion.route("/cualquier-rol")
    @sistema.requiere_rol()
    def cualquier_rol():
        return jsonify({"ok": True})

    @aplicacion.route("/entrar/<rol>")
    def entrar(rol):
        session["usuario"] = {
            "id": 1,
            "nombre": rol,
            "correo": f"{rol}@test.local",
            "rol": rol,
            "perfil": rol,
        }
        return jsonify({"ok": True})

    return aplicacion


@pytest.fixture
def cliente_permisos():
    return app_con_permisos().test_client()


def test_requiere_rol_sin_sesion_devuelve_401(cliente_permisos):
    # Arrange
    destino = "/solo-admin"
    # Act
    respuesta = cliente_permisos.get(destino)
    # Assert
    assert respuesta.status_code == 401
    assert respuesta.json["error"] == "Debes iniciar sesión"


def test_requiere_rol_deniega_rol_no_autorizado(cliente_permisos):
    # Arrange
    cliente_permisos.get("/entrar/vendedor")
    # Act
    respuesta = cliente_permisos.get("/solo-admin")
    # Assert
    assert respuesta.status_code == 403


def test_requiere_rol_permite_rol_autorizado(cliente_permisos):
    # Arrange
    cliente_permisos.get("/entrar/admin")
    # Act
    respuesta = cliente_permisos.get("/solo-admin")
    # Assert
    assert respuesta.status_code == 200
    assert respuesta.json["ok"] is True


def test_requiere_rol_admite_multiples_roles(cliente_permisos):
    # Arrange
    cliente_permisos.get("/entrar/vendedor")
    # Act
    respuesta = cliente_permisos.get("/admin-o-vendedor")
    # Assert
    assert respuesta.status_code == 200


def test_requiere_rol_sin_argumentos_solo_exige_sesion(cliente_permisos):
    # Arrange
    cliente_permisos.get("/entrar/compras")
    # Act
    respuesta = cliente_permisos.get("/cualquier-rol")
    # Assert
    assert respuesta.status_code == 200
