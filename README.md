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
	},
	"product-data-api":{
		port: 9002
	}
}
```
***

example:
    
    node api: http://localhost:9000/user/10/post
    python api: http://localhost:9002/products/10-ab

    with gateway: http://localhost:8000/user-data-api/user/10/post
    with gateway: http://localhost:8000/product-data-api/products/10-ab
    
    
    
### ovio, this makes core apis slow, but you get alot of flexibility, plus you must also look how to make fast apis fast, cause in general fast api's development is fast, execution is slow like flask and other python framework.
###  future: will add put and delete methods.
