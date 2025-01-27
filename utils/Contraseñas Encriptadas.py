import bcrypt

hashed_password = bcrypt.hashpw("12345A".encode(), bcrypt.gensalt()).decode()
print(hashed_password)
