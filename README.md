# Api Gateway
### _with fastAPI_

>Just Define your damm api in **endpoint_defination.py** file, and you're good to go.

```
endpoint_definations = {
	"user-data-api": {
		"host": "localhost",
		"port": "8000",
		"auth": {
			"GET": {
				"required" : True
			},
			"POST": {
				"required" : False
			}
		},
		"excluded_routes": [
			("GET", "admin/:user_id"),
			("POST", "admin/:user_id"),
			("POST", "admin/:user_id/posts"),
            # ROUTES HERE WONT REQUIRE JWT CHECK, even though all POST/GET req requires VALIDATION
		]
	}
}
```
***

example:
    
    node api: http://localhost:9000/user/10/post

    with gateway: http://localhost:8000/user-endpoint-api/user/10/post
