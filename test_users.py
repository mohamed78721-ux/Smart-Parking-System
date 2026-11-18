from users import add_user, view_users

if __name__ == "__main__":
    add_user("mohamed", "hashed_password", "Mohamed Hassan", "0987654321", "staff", "active")
    view_users()
