# fastapi-apigateway

in endpoint_defination.py, add your apis, put if it needed jwt authentication or not.

add endpoint in endpoint_definations = {
    "api-endpoint-name":{
        "host": "where it is running",
        "port": "on which port",
        "auth": {
            "GET": "Does all req of this api new jwt verification",
            "POST": "Does all req of this api new jwt verification"
        }
    }
}

example:
    node api : http://localhost:9000/user/10/post

    with gateway: http://localhost:8000/user-endpoint-api/user/10/post