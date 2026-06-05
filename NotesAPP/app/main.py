from fastapi import FastAPI
from routes.notes_routes import router
app=FastAPI()
app.include_router(router)
