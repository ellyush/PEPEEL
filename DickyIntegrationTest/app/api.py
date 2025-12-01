from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from .session import Session
from .auth import AuthService
from .dataset import DatasetService, Dataset
from .forum import ForumService
from .exceptions import (
    AuthError, RegisterError, DatasetError,
    OAuthNotSupported, VerificationError, ForumError
)

app = FastAPI(title="Integration Test API")

session = Session()
auth_service = AuthService(session)
dataset_service = DatasetService(session)
forum_service = ForumService(session)


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
        return forum_service.create_forum(
            data.title,
            data.content,
            data.tags
        )
    except (AuthError, ForumError) as e:
        raise HTTPException(status_code=400, detail=str(e))
