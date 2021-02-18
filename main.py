from app import app
import uvicorn
from config import config


if __name__ == '__main__':
    uvicorn.run(app, port=config.PORT, host=config.HOST)