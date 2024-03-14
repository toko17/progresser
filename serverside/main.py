from fastapi import FastAPI
from routers import users, token, organisations
# organisations, tables, lists, tasks, subtasks,

import models
from database import engine

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Progresser API',
    description="API Docs",
    version="0.1"
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(token.router)
app.include_router(users.router)
app.include_router(organisations.router)
# app.include_router(tables.router)
# app.include_router(lists.router)
# app.include_router(tasks.router)
# app.include_router(subtasks.router)
