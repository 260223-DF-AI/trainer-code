from fastapi import FastAPI
from .routers import salesroutes

app = FastAPI(
    title = "Sales API",
    description = "API for Sales Data",
    version = "0.0.1"
)

app.include_router(salesroutes.router)

@app.get("/")
def get_root():
    return {"message": "Hello from main"}