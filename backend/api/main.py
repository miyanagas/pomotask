from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.database import create_db_and_tables, drop_db_and_tables
from api.routers import auth, users, todo_list

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")

# CORSの設定
origins = [
    "https://todo-app-2yl.pages.dev",
    "https://miyanagas.github.io",
    # "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(todo_list.router)

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()[0].get("msg")}),
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# @app.on_event("shutdown")
# def on_shutdown():
#     drop_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}