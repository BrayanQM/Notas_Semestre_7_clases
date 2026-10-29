```bash
num1 = int(input("Ingrese num1: "))
num2 = int(input("Ingrese num2: "))
num3 = int(input("Ingrese num3: "))

entrada = np.array([[num1, num2, num3]],dtype=np.int16)

prediccion = model.predict(
    entrada,
    verbose=0
)

resultado = prediccion[0][0]

print(
    f"\nPredicción de la red: "
    f"{resultado:.4f}"
)

print(
    f"Resultado entero: "
    f"{round(resultado)}"
)
```
-  otra parte del codigo de prueba 
```bash
redicciones = model.predict(
    X_test,
    verbose=0
).flatten()

for i in range(len(X_test)):

    entrada = X_test.iloc[i].values

    real = y_test.iloc[i]

    prediccion = predicciones[i]

    prediccion_redondeada = round(
        prediccion
    )

    print(
        f"Entrada: "
        f"| Real={real:.0f} "
        f"| Predicción={prediccion:.4f} "
        f"| Redondeada={prediccion_redondeada}"
    )
    ```