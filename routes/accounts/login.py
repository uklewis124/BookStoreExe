from routes.accounts import accounts

REGISTER_ROUTE = "/login/"
ALLOWED_METHODS = ["GET", "POST"]

@accounts.route(REGISTER_ROUTE, methods=ALLOWED_METHODS)
def login():
    return "login"