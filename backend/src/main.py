from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.parser import dpkg_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


status = dpkg_status("resources/status.dummy")

@app.get("/package_list")
async def package_list():
    return { "package_list": status.get_package_list() }

@app.get("/package/{package}")
async def package(package: str):
    return status.get_package(package)
