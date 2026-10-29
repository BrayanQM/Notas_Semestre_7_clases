import os

# Asegura DISPLAY para entorno gráfico (Wayland+Xwayland)
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":1"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

_orig_chrome = webdriver.Chrome

# Usamos Brave Origin Nightly (Chromium fork). El chromedriver cacheado coincide en major version (155.x).
CHROME_BIN = "/usr/bin/brave-origin-nightly"
DRIVER_BIN = os.path.expanduser("~/.cache/selenium/chromedriver/linux64/155.0.8059.39/chromedriver")

def chrome_patched(*args, **kwargs):
    opts = Options()
    opts.binary_location = CHROME_BIN
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    svc = Service(executable_path=DRIVER_BIN)
    if "options" not in kwargs:
        kwargs["options"] = opts
    else:
        # Mezcla con opciones existentes
        kwargs["options"] = kwargs["options"]
        # Asegura binary_location
        kwargs["options"].binary_location = CHROME_BIN
    if "service" not in kwargs:
        kwargs["service"] = svc
    return _orig_chrome(*args, **kwargs)

webdriver.Chrome = chrome_patched
