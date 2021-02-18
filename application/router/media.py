from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile
import requests
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
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
from PIL import Image, ImageOps, ImageChops
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

        # Thumbnail
        size = (300,300)
        antiAliasedImage.thumbnail(size, Image.ANTIALIAS)
        image_size = antiAliasedImage.size

        thumb = antiAliasedImage.crop( (0, 0, size[0], size[1]) )
        offset_x = int(max( (size[0] - image_size[0]) / 2, 0 ))
        offset_y = int(max( (size[1] - image_size[1]) / 2, 0 ))

        thumb = ImageChops.offset(thumb, offset_x, offset_y)
        thumb.save(os.path.join(config.thumbnail_path, imageName))
        
    except Exception as e:
        print(e)

@router.post("/media/upload")
async def mediaUpload(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...)):
    try:
        imgType = imghdr.what(image.file)
        if not (imgType == "png" or imgType == "jpeg"):
            raise HTTPException(status_code=404, 
                detail="Image Files only Allowed (JPEG AND PNG)")
        fileName = str(uuid.uuid4()) + '.{}'.format(imgType)
        serverDestination = open(os.path.join(config.media_path, fileName), 'wb+')
        shutil.copyfileobj(image.file, serverDestination)
        serverDestination.close()
        background_tasks.add_task(imageCompression, imageName=fileName)
        return {
            "file_name": fileName,
            "preview": "http://{}:{}/media/{}/original".format("localhost", "8080",fileName),
            "thumbnail_preview": "http://{}:{}/media/{}/thumb".format("localhost", "8080",fileName)
        }
    except HTTPException as e:
        return {
            "error": e
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    
@router.get("/media/{imageFileName:str}/{format:str}")
async def getImage(request: Request, imageFileName: str, format: str):
    try:
        if not os.path.isfile(config.media_path + imageFileName):
            raise HTTPException(status_code=404, 
                detail="This File Doesn't Exsits")
        if format == "thumb":
            return FileResponse(config.thumbnail_path + imageFileName)
        return FileResponse(config.media_path + imageFileName)
    except HTTPException as e:
        return {
            "error": e
        }
    except Exception as e:
        return {
            "error": str(e)
        }
