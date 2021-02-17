endpoint_definations = {
	"user-data-api": {
		"host": "localhost",
		"port": "8000",
		"auth": {
			"GET": {
				"required" : True
			},
			"POST": {
				"required" : True
			}
		},
		"excluded_routes": [
			"admin/:user_id",
			"admin/:user_id/posts"
		]
	}
}