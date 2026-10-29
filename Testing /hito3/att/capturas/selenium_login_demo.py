import os
import time

os.environ.setdefault("DISPLAY", ":1")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROME_BIN = "/usr/bin/brave-origin-nightly"
DRIVER_BIN = os.path.expanduser(
    "~/.cache/selenium/chromedriver/linux64/155.0.8059.39/chromedriver"
)
CAPTURAS = "/home/eynor/Documents/semestr7/Testing /hito3/att/capturas"

opciones = Options()
opciones.binary_location = CHROME_BIN
opciones.add_argument("--no-sandbox")
opciones.add_argument("--disable-dev-shm-usage")
opciones.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(executable_path=DRIVER_BIN), options=opciones
)
espera = WebDriverWait(driver, 20)

driver.get("http://127.0.0.1:5000")
espera.until(EC.visibility_of_element_located((By.ID, "correo-login")))

campo_correo = driver.find_element(By.ID, "correo-login")
campo_contrasena = driver.find_element(By.ID, "contrasena-login")

campo_correo.clear()
campo_correo.send_keys("pedrito@gmail.com")
time.sleep(0.5)
campo_contrasena.clear()
campo_contrasena.send_keys("bolivia123")
time.sleep(0.5)

# Verificacion de que los datos quedaron escritos antes de capturar.
assert campo_correo.get_attribute("value") == "pedrito@gmail.com"
assert campo_contrasena.get_attribute("value") == "bolivia123"

driver.save_screenshot(os.path.join(CAPTURAS, "02_selenium_login_form_view.png"))
print("Credenciales escritas y verificadas en el formulario.", flush=True)

# Pausa larga con el formulario ya lleno: aqui se toma la captura de pantalla.
time.sleep(28)

driver.find_element(
    By.CSS_SELECTOR, "#form-login button[type='submit']"
).click()
espera.until(EC.visibility_of_element_located((By.ID, "vista-app")))

usuario = driver.find_element(By.ID, "usuario-nombre").text
perfil = driver.find_element(By.ID, "usuario-perfil").text
print(f"Login OK -> {usuario} ({perfil})", flush=True)

driver.save_screenshot(os.path.join(CAPTURAS, "03_selenium_app.png"))
time.sleep(8)
driver.quit()
