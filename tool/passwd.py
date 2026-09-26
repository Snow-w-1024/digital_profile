import os
import sys

import bcrypt

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

if __name__ == "__main__":
    password = os.environ.get("ADMIN_PASSWORD")
    if password is None:
        password = sys.argv[1] if len(sys.argv) > 1 else input()
    hashed_password = hash_password(password)
    print(hashed_password)