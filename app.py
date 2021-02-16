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

app = FastAPI(debug=True)

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
			if(endpoint_def["auth"][method]["required"]):
				jwtToken = request.headers["www-authenticate"]
				payload = jwt.decode(jwtToken, config.SECRET_KEY,  algorithms=[config.ALGORITHM])
				
			forwarding_url = ("http://{}:{}/{}".format(endpoint_def["host"], endpoint_def["port"],'/'.join(endpoint_url[1:])))
			req = requests.get(forwarding_url)
			return json.loads(req.content)
		else:
			raise HTTPException(status_code=404, detail="Route Not Present")
	
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
			if(endpoint_def["auth"][method]["required"]):
				jwtToken = request.headers["www-authenticate"]
				payload = jwt.decode(jwtToken, config.SECRET_KEY,  algorithms=[config.ALGORITHM])
			forwarding_url = ("http://{}:{}/{}".format(endpoint_def["host"], endpoint_def["port"],'/'.join(endpoint_url[1:])))
			req = requests.post(forwarding_url, json=jsonable_encoder(inputParam))
			return json.loads(req.content)
		else:
			raise HTTPException(status_code=404, detail="Route Not Present")

	except Exception as e:
		return {
			"error": {
				"status": True,
				"message": str(e),
				"code": 500
			}
		}