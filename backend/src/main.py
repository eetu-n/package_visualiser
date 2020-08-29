from fastapi import FastAPI
from src.parser import dpkg_status

app = FastAPI()

status = dpkg_status("resources/status.dummy")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/package_list")
async def package_list():
    return status.get_package_list()

@app.get("/packages/{package}")
async def package(package: str):
    return status.get_package(package)
