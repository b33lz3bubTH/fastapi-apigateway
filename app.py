from fastapi import FastAPI, Request, HTTPException, status
import requests
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from application import getRoutes
from pydantic import BaseModel
import json
from endpoint_definations import endpoint_definations
from config import config
import jwt

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from utils import exclusion_check

class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return await call_next(request)

app = FastAPI(debug=True)
app.add_middleware(LimitUploadSize, max_upload_size=3_000_000)

routerPaths = getRoutes()
for routerPath in routerPaths:
	app.include_router(routerPath)

@app.get("/{url:path}")
async def GETApiGateway(request: Request, url: str):
	try:
		method = "GET"
		endpoint_url = url.split("/")
		endpoint_def = endpoint_definations.get(endpoint_url[0])
		if endpoint_def:
			if not exclusion_check(endpoint_def["excluded_routes"], endpoint_url[1:]):
				if(endpoint_def["auth"][method]["required"]):
					jwtToken = request.headers["www-authenticate"]
					payload = jwt.decode(jwtToken, config.SECRET_KEY,  algorithms=[config.ALGORITHM])
				
			forwarding_url = ("http://{}:{}/{}".format(endpoint_def["host"], endpoint_def["port"],'/'.join(endpoint_url[1:])))
			req = requests.get(forwarding_url)
			return json.loads(req.content)
		else:
			raise Exception("Route Not Present")
	
	except Exception as e:
		return {
			"error": {
				"status": True,
				"message": str(e),
				"code": 500
			}
		}

@app.post("/{url:path}")
async def POSTApiGateway(request: Request, url: str):
	try:
		inputParam = json.loads((await request.body()).decode('utf-8'))
		method = "POST"
		endpoint_url = url.split("/")
		endpoint_def = endpoint_definations.get(endpoint_url[0])
		if endpoint_def:
			if not exclusion_check(endpoint_def["excluded_routes"], endpoint_url[1:]):
				if(endpoint_def["auth"][method]["required"]):
					jwtToken = request.headers["www-authenticate"]
					payload = jwt.decode(jwtToken, config.SECRET_KEY,  algorithms=[config.ALGORITHM])
			forwarding_url = ("http://{}:{}/{}".format(endpoint_def["host"], endpoint_def["port"],'/'.join(endpoint_url[1:])))
			req = requests.post(forwarding_url, json=jsonable_encoder(inputParam))
			return json.loads(req.content)
		else:
			raise Exception("Route Not Present")


	except Exception as e:
		return {
			"error": {
				"status": True,
				"message": str(e),
				"code": 500
			}
		}