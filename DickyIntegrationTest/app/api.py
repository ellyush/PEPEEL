from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from .firebase_client import init_firebase
from .auth_firebase import AuthService
from .dataset_firebase import DatasetService
from .dataset import Dataset
from .forum_firebase import ForumService
from .session import Session
from .exceptions import (
    AuthError, RegisterError, DatasetError,
    OAuthNotSupported, VerificationError, ForumError
)

app = FastAPI(title="Integration Test API")

db = init_firebase()  # inisialisasi sekali

session = Session()
auth_service = AuthService(session, db=db)
dataset_service = DatasetService(session, db=db)
forum_service = ForumService(session, db=db)

# ---------- SCHEMAS ----------
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    fullname: str
    recaptcha: bool = True
    receive_news: bool = False

class PhoneRequest(BaseModel):
    phone: str
    fullname: str = ""


class FaceVerificationRequest(BaseModel):
    phone: str
    persona_payload: dict

class DatasetRequest(BaseModel):
    name: str
    source_type: str
    size: Optional[int] = None
    link: Optional[str] = None

class ForumRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = []


# ---------- AUTH ----------
@app.post("/login")
def login(data: LoginRequest):
    try:
        return auth_service.login(data.email, data.password)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/register")
def register(data: RegisterRequest):
    try:
        return auth_service.register(
            data.email,
            data.password,
            data.fullname,
            data.recaptcha,
            data.receive_news
        )
    except RegisterError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/logout")
def logout():
    try:
        auth_service.logout()
        return {"message": "Logged out"}
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ---------- PHONE & FACE ----------
@app.post("/auth/phone")
def create_user_phone(data: PhoneRequest):
    try:
        return auth_service.create_user_with_phone(data.phone, data.fullname)
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/phone/verify")
def verify_phone(phone: str):
    try:
        return {"message": auth_service.verify_phone(phone)}
    except VerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/face/verify")
def verify_face(data: FaceVerificationRequest):
    try:
        return {
            "message": auth_service.verify_face(
                data.phone,
                data.persona_payload
            )
        }
    except VerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- DATASET ----------
@app.post("/dataset")
def create_dataset(data: DatasetRequest):
    try:
        dataset = Dataset(
            name=data.name,
            source_type=data.source_type,
            size=data.size,
            link=data.link
        )
        return {"message": dataset_service.create_dataset(dataset)}
    except DatasetError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- FORUM ----------
@app.post("/forum")
def create_forum(data: ForumRequest):
    try:
        # pass auth_service supaya forum service bisa cek verifikasi penuh
        return forum_service.create_forum(
            data.title,
            data.content,
            data.tags,
            auth_service
        )
    except (AuthError, ForumError) as e:
        raise HTTPException(status_code=400, detail=str(e))
