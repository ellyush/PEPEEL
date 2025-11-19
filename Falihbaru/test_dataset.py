import unittest
from dataset import upload_dataset, create_from_notebook

class TestDataset(unittest.TestCase):

    # TC-35 upload dataset berbagai format
    def test_upload_dataset_formats(self):
        for f in ["csv", "zip", "json"]:
            self.assertEqual(upload_dataset(f), "Upload sukses")

    # TC-36 upload dataset berbagai ukuran file
    def test_upload_dataset_small_size(self):
        self.assertEqual(upload_dataset("csv", file_size_mb=1),
                          "Upload sukses")

    def test_upload_dataset_medium_size(self):
        self.assertEqual(upload_dataset("csv", file_size_mb=50),
                          "Upload sukses")

    def test_upload_dataset_large_size(self):
        self.assertEqual(upload_dataset("csv", file_size_mb=250),
                          "File terlalu besar")

    # TC-37 upload dataset dari link public
    def test_upload_dataset_public_link(self):
        self.assertEqual(upload_dataset("csv", link="http://example.com", is_private=False), 
                         "Upload dari link sukses")

    # TC-38 upload dataset dari link private
    def test_upload_dataset_private_link(self):
        self.assertEqual(upload_dataset("csv", link="http://example.com", is_private=True), 
                         "Link tidak bisa diakses")

    # TC-39 membuat dataset dari notebook
    def test_create_from_notebook(self):
        self.assertEqual(create_from_notebook(), "Dataset dari notebook berhasil")

if __name__ == "__main__":
    unittest.main()
