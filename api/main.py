from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from backend.pipeline import run_pipeline
from backend.database import init_db
from backend.pdf_generator import generate_mom_pdf
from fastapi.responses import FileResponse
from fastapi import Form
from fastapi.responses import RedirectResponse
from backend.auth import register_user, authenticate_user





# ---------------- INIT ----------------
app = FastAPI(title="InsightMeet")

init_db()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "data/uploads"
MOM_DIR = "data/mom"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MOM_DIR, exist_ok=True)

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------------- PROCESS MEETING ----------------
@app.post("/process", response_class=HTMLResponse)
async def process_meeting(request: Request, file: UploadFile = File(...)):
    audio_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # Run full ML pipeline
    result = run_pipeline(audio_path)

    # Generate MOM PDF
    generate_mom_pdf(
        output_path=os.path.join(MOM_DIR, "meeting_mom.pdf"),
        meeting_title="Project Meeting",
        transcript=result["transcript"],
        summary=result["summary"],
        action_items=[],
        impact_points=result["impact_points"]
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": result["summary"],
            "recap": result["recap"],
            "transcript": result["transcript"],
            "impact": result["impact_points"],
            "pdf_ready": True
        }
    )

# ---------------- DOWNLOAD PDF ----------------
@app.get("/download")
def download_pdf():
    return FileResponse(
        "data/mom/meeting_mom.pdf",
        media_type="application/pdf",
        filename="Minutes_of_Meeting.pdf"
    )

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")
# ---------------- AUTHENTICATION ----------------

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        response = RedirectResponse("/", status_code=302)
        response.set_cookie("user", username)
        return response
    return RedirectResponse("/login", status_code=302)

@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("user")
    return response


