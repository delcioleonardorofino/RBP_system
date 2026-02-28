from fastapi import FastAPI
import api.v1.router.auth_router as auth_router
import api.v1.router.secretaria_router as secretaria_router
import api.v1.router.bootstrap as bootstrap_router
import api.v1.router.super_admin_router as super_admin_router
import api.v1.router.admin_router as admin_router
from database.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(bootstrap_router.router)
app.include_router(secretaria_router.router)
app.include_router(super_admin_router.router)
app.include_router(admin_router.router)

@app.get('/')
def home():
    return 'This is home!'

