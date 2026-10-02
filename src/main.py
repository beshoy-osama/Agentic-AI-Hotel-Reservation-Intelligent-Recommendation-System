from fastapi import FastAPI
from routes import health
from routes import agent
from helpers import get_settings


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Application is starting up...")

    settings = get_settings()


    yield

    print("Closed all connections cleanly.")

app = FastAPI(lifespan=lifespan)

app.include_router(health.health_router)
app.include_router(agent.agent_router)
