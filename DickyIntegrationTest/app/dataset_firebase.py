# dataset_firebase.py
from .exceptions import DatasetError
from .firebase_client import init_firebase

class DatasetService:
    def __init__(self, session, db=None):
        self.session = session
        self.db = db or init_firebase()
        self.datasets_col = self.db.collection("datasets")

    def create_dataset(self, dataset):
        if not self.session.is_logged_in():
            raise DatasetError("You must be logged in to create a dataset")

        # build dataset doc
        owner_key = self.session.get_user_key()
        doc_data = {
            "name": dataset.name,
            "source_type": dataset.source_type,
            "size": dataset.size,
            "link": dataset.link,
            "owner": owner_key
        }
        # let Firestore generate id
        self.datasets_col.add(doc_data)
        return "Success, Your dataset was created successfully."
