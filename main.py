from fastapi import FastAPI
from routers import admin, user, client, company

app = FastAPI()


app_admin = FastAPI(title="Admin API", version="1")
app_client = FastAPI(title="Client API", version="1")
app_user = FastAPI(title="User API", version="1")

app.mount("/admin", app_admin)
app_admin.include_router(admin.router)

app.mount("/user", app_user)
app_user.include_router(user.router)

app.mount("/client", app_client)
app_client.include_router(client.router)
app_client.include_router(company.router)