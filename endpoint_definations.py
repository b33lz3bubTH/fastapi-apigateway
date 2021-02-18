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
			# ("GET", "admin/:user_id"),
			# ("POST", "admin/:user_id"),
			# ("POST", "admin/:user_id/posts")
		]
	}
}