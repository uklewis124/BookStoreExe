from routes.accounts import accounts

REGISTER_ROUTE = "/register/"
ALLOWED_METHODS = ["GET", "POST"]

@accounts.route(REGISTER_ROUTE, methods=ALLOWED_METHODS)
def register():
    return "Register"