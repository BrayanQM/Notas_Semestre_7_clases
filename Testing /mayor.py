def validar_contrasena(password):
    """
    Devuelve True si la contraseña tiene exactamente 8 caracteres
    y contiene solo letras y números (sin caracteres especiales).
    """
    # len(password) == 8 verifica la longitud exacta
    # password.isalnum() verifica que no tenga símbolos ni espacios
    return len(password) == 8 and password.isalnum()

# 1. PRUEBA AUTOMÁTICA CON LOS DATOS DE TU TABLA
tabla_ejemplos = [
    {"id": 1, "password": "holaPat1"},  # True: Alfanumérico y 8 caracteres
    {"id": 2, "password": "047293Ea"},  # True: Alfanumérico y 8 caracteres
    {"id": 3, "password": "g83r4132"},  # True: Alfanumérico y 8 caracteres
    {"id": 4, "password": "ubv31eu9"},  # True: Alfanumérico y 8 caracteres
    {"id": 5, "password": "12345678"},  # True: Alfanumérico y 8 caracteres
    {"id": 6, "password": "@@@@@@@@"},  # False: Tiene caracteres especiales
    {"id": 7, "password": "abc45"},     # False: Es muy corta (5 caracteres)
    {"id": 8, "password": "pass123456"}  # False: Es muy larga (10 caracteres)
]

print("--- EJECUTANDO PRUEBA DE LA TABLA ---")
print(f"{'ID':<5} | {'Contraseña':<12} | {'Resultado':<6}")
print("-" * 32)

for fila in tabla_ejemplos:
    res = validar_contrasena(fila["password"])
    print(f"{fila['id']:<5} | {fila['password']:<12} | {str(res):<6}")

print("\n" + "="*40 + "\n")

# 2. PRUEBA INTERACTIVA CON EL USUARIO
print("--- PRUEBA DE USUARIO EN VIVO ---")
usuario_password = input("Escriba su contraseña (debe tener exactamente 8 caracteres): ")

# Evaluamos la entrada del usuario
if validar_contrasena(usuario_password):
    print("Resultado: True (Contraseña aceptada)")
else:
    print("Resultado: False (Contraseña rechazada: debe medir 8 caracteres y no usar símbolos)")
