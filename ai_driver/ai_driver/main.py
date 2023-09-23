from ai_driver.config import server_config
from ai_driver.server.server import app
from loguru import logger
import uvicorn

logger.info(server_config)

if __name__ == "__main__":
    # Use this for debugging purposes only

    logger.info("Starting uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=28001, log_level=server_config.LOG_LEVEL)
