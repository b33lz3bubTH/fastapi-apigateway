from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile
import requests
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from typing import Optional
from pydantic import BaseModel
from config import config
import jwt
import os
import uuid
import shutil
import imghdr
from PIL import Image
import math
import time

router = APIRouter()

def imageCompression(imageName: str = None):
    try:
        originalImage = Image.open(os.path.join(config.media_path, imageName))
        x, y = originalImage.size
        x2, y2 = math.floor(x-50), math.floor(y-20)
        antiAliasedImage = originalImage.resize((x2,y2),Image.ANTIALIAS)
        antiAliasedImage.save(os.path.join(config.media_path, imageName), quality=60, optimize=True)
    except Exception as e:
        pass

@router.post("/media/upload")
async def mediaUpload(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...)):
    try:
        imgType = imghdr.what(image.file)
        if not (imgType == "png" or imgType == "jpeg"):
            raise Exception("Image Files only Allowed (JPEG AND PNG)")
        fileName = str(uuid.uuid4()) + '.{}'.format(imgType)
        serverDestination = open(os.path.join(config.media_path, fileName), 'wb+')
        shutil.copyfileobj(image.file, serverDestination)
        serverDestination.close()
        background_tasks.add_task(imageCompression, imageName=fileName)
        return {
            "file_name": fileName
        }
    except Exception as e:
        return {
			"error": {
				"status": True,
				"message": str(e),
				"code": 500
			}
		}
    