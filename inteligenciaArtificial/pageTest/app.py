from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from models import predict_max

BASE_DIR = Path(__file__).parent
app = FastAPI(title="Unifranz")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"result": None})


@app.post("/enviar", response_class=HTMLResponse)
def enviar(
    request: Request,
    num1: int = Form(...),
    num2: int = Form(...),
    num3: int = Form(...),
):
    result = predict_max(num1, num2, num3)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "num1": num1,
            "num2": num2,
            "num3": num3,
            "result": result,
        },
    )