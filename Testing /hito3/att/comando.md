cd '/home/eynor/Documents/semestr7/Testing /hito3/att'
pip install pytest selenium

export BASE_URL='https://kqrcxvlm-5000.brs.devtunnels.ms/'
export TEST_EMAIL='brayan.quispe.2@gmail.com'
export NOMBRE_COMPLETO='Brayan Quispe Mamani'
read -s bolivia123
export bolivia123
pytest -v -s test_producto.py
