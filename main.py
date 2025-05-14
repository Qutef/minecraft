from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

with open("data.json", encoding="utf-8") as f:
    sounds = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "sounds": sounds})

@app.get("/sound/{sound_id}", response_class=HTMLResponse)
async def sound_page(request: Request, sound_id: str):
    sound = next((s for s in sounds if s["id"] == sound_id), None)
    if not sound:
        return HTMLResponse("Not found", status_code=404)
    return templates.TemplateResponse("sound.html", {"request": request, "sound": sound})
