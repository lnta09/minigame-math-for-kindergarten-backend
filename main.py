from fastapi import FastAPI, Depends, HTTPException, Query
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from db import create_db_and_tables, get_session
from level import router as level_router

app = FastAPI()
DIRECTORY = os.getcwd()

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(level_router)