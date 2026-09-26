import os
import jwt
import bcrypt
import uvicorn
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient


app = FastAPI()

SECRET_KEY = os.environ.get("SECRET_KEY", "default_jwt_secret_key")
ALGORITHM = "HS256"
ADMIN_HASH = os.environ.get("ADMIN_HASH", "$2b$12$placeholder_hash_string_replace_me").encode("utf-8")

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client.profile_db
collection = db.profiles_data

if collection.count_documents({}) == 0:
    collection.insert_one({
        "message": "Hello, World!",
        "name": ".w.",
        "bio": "this is a test text",
        "skills": "do this, do that"
    })

class ProfileUpdate(BaseModel):
    name: str
    message: str
    bio: str
    skills: str

class LoginRequest(BaseModel):
    password: str

@app.get("/api/profile")
async def get_profile():
    profile = collection.find_one({}, {"_id": 0})
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.post("/api/login")
async def login(req: LoginRequest):
    input_pwd_bytes = req.password.encode("utf-8")
    
    try:
        is_valid = bcrypt.checkpw(input_pwd_bytes, ADMIN_HASH)
    except ValueError:
        is_valid = False

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode = {"sub": "admin", "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token": encoded_jwt}

@app.put("/api/profile")
async def update_profile(profile_data: ProfileUpdate, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    collection.update_one({}, {"$set": profile_data.model_dump()})
    return {"status": "success"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)