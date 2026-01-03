from models.user import User

# Mock users (replace with DB later)
users = [
    User(1, "admin", "admin123", "ADMIN"),
    User(2, "operator", "operator123", "OPERATOR")
]

def authenticate(username, password):
    for user in users:
        if user.username == username and user.check_password(password):
            return user
    return None
