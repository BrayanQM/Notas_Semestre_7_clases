import numpy as np
from keras.models import load_model
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "modelo_mayor.keras"

model = load_model(MODEL_PATH)


def predict_max(num1: int, num2: int, num3: int) -> int:
    entrada = np.array([[num1, num2, num3]], dtype=np.int16)
    prediccion = model.predict(entrada, verbose=0)[0][0]
    return int(round(prediccion))