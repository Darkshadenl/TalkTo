from fastapi import FastAPI
from .core.config import settings
from .api.endpoints import router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE, version=settings.API_VERSION, debug=settings.DEBUG
)

# Log watched folders during startup
logger.info("Loaded Watched Folders:")
for folder in settings.WATCHED_FOLDERS:
    logger.info(
        f"- {folder.name}: {folder.path} ({folder.description or 'No description'})"
    )

# Log API token for authentication
logger.info("API Token for authentication:")
logger.info(f"X-API-Token: {settings.API_TOKEN}")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
