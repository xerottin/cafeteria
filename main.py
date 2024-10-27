from fastapi import FastAPI
from routers import admin
app = FastAPI()


app_admin = FastAPI(title="Admin API", version="1")
app_client = FastAPI(title="Client API", version="1")
app_user = FastAPI(title="User API", version="1")

app.mount("/admin", app_admin)
app_admin.include_router(admin.router)