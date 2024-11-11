import pytz
from fastapi import FastAPI
from routers import admin, user, cafeteria, company, user_cafeteria, cafeteria_menu
from auth.authentication import router as admin_auth_router

uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
app = FastAPI()


app.include_router(admin_auth_router)
app_admin = FastAPI(title="Admin API", version="1")
app_cafeteria = FastAPI(title="Cafeteria API", version="1")
app_user = FastAPI(title="User API", version="1")

app.mount("/admin", app_admin)
app_admin.include_router(admin_auth_router)
app_admin.include_router(admin.router)
app_admin.include_router(company.router)

app.mount("/cafeteria", app_cafeteria)
app_cafeteria.include_router(admin_auth_router)
app_cafeteria.include_router(cafeteria.router)
app_cafeteria.include_router(cafeteria_menu.router)

app.mount("/user", app_user)
app_user.include_router(admin_auth_router)
app_user.include_router(user.router)
app_user.include_router(user_cafeteria.router)
