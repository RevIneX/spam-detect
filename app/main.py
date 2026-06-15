from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from app.routes import analyze, history
from app.init_db import init_db
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Spam Detector", version="1.0.0")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    logger.info("Starting application...")
    init_db()
    logger.info("Application started")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(analyze.router, tags=["Analyze"])
app.include_router(history.router, tags=["History"])

@app.exception_handler(SQLAlchemyError)
async def handle_db_error(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {exc}")
    raise HTTPException(status_code=500, detail="Database connection error")
