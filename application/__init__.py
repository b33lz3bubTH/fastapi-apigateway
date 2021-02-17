from application.router import auth, media

def getRoutes():
	return [
		auth.router,
		media.router
	]