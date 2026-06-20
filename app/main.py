from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import contacts, orders, auth

from app import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # instead of * should be the telegram domen
    allow_credentials=True,
    allow_methods=["*"], # permit all HTTP methods and headers
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

 