from fastapi import FastAPI
from app.routers.contacts import router

app = FastAPI()
app.include_router(router)
@app.get('/')
def home():
    return {"message": "This is home page"}
