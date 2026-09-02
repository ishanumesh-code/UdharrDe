import os
import sys


FASTAPI_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(FASTAPI_DIR)

if FASTAPI_DIR not in sys.path:
    sys.path.insert(0, FASTAPI_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from router.auth.auth import auth_router
from router.dashboard.home import home as dashboard_router
from router.group.groups import groups as group_router
from router.expenses.expenses import expenses as expenses_router

app = FastAPI(title="UdharrDe")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For UI test only
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

static_dir = os.path.join(FASTAPI_DIR, "static")
ui_file = os.path.join(static_dir, "ui.html")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(group_router)
app.include_router(expenses_router)

@app.get("/")
def read_root():
    # For UI test only
    if os.path.exists(ui_file):
        return FileResponse(ui_file)
    return {"messages": "API is Running perfectly."}


