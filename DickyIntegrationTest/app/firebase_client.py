# firebase_client.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase(service_account_path: str = "D:/Semester 3/Pengujian Perangkat Lunak/PEPEEL/DickyIntegrationTest/app/pepeel-firebase-adminsdk-fbsvc-808ec24bb8.json"):
    """
    Jika service_account_path None, firebase-admin akan
    memakai env var GOOGLE_APPLICATION_CREDENTIALS jika tersedia.
    """
    if not firebase_admin._apps:
        if service_account_path:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    return firestore.client()

# contoh pemakaian:
# db = init_firebase("path/to/serviceAccount.json")
# atau set env var: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccount.json"
