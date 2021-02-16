from application.router import auth

def getRoutes():
	return [
		auth.router
	]