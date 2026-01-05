from models.user import User

# Mock users (replace with DB later)
# Default password for all users: Group5
users = [
    User(1, "admin", "Group5", "ADMIN"),
    User(2, "operator", "Group5", "OPERATOR")
]

def authenticate(username, password):
    for user in users:
        if user.username == username and user.check_password(password):
            return user
    return None
