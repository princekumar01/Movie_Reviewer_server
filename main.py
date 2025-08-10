from fastapi import FastAPI
import models
from database import engine
from routers import user, movie, reviewer

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(movie.router)
app.include_router(reviewer.router)
