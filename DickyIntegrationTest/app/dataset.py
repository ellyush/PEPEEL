from .exceptions import DatasetError

class Dataset:
    def __init__(self, name, source_type, size=None, link=None):
        self.name = name
        self.source_type = source_type  # "csv", "json", "zip", "notebook_output", "public_link", "private_link"
        self.size = size
        self.link = link


class DatasetService:
    def __init__(self, session):
        self.session = session
        self.datasets = []

    def create_dataset(self, dataset: Dataset):
        if not self.session.is_logged_in():
            raise DatasetError("You must be logged in to create a dataset")

        if dataset.source_type == "private_link":
            raise DatasetError("Link is Private")

        self.datasets.append(dataset)
        return "Success, Your dataset was created successfully."
