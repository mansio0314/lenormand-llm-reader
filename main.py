from fastapi import FastAPI, Request                 # ← Request 추가
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse           # ← 추가
from fastapi.staticfiles import StaticFiles          # ← 추가
from fastapi.templating import Jinja2Templates       # ← 추가

from api.reading import router as reading_router


app = FastAPI(title="Lenormand LLM Reader", version="0.1.0")

# --- 1) 템플릿 & 정적 파일 설정 -----------------------------------
templates = Jinja2Templates(directory="templates")   # ← templates 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")  # ← static 폴더 연결
# ------------------------------------------------------------------


# CORS (지금은 프로토타입이라 널널하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터
app.include_router(reading_router)


# --- 2) 프런트엔드를 보여주는 기본 페이지 --------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("reading.html", {"request": request})
# ------------------------------------------------------------------


# 헬스체크
@app.get("/health")
async def healthcheck() -> dict:
    return {"status": "ok"}
