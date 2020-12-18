from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routers.user_router import router as router_users
from routers.transaction_router import router as router_transactions

mi_app = FastAPI()

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "https://cajero-app-frontend-77.herokuapp.com"
]
mi_app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

mi_app.include_router(router_users)
mi_app.include_router(router_transactions)