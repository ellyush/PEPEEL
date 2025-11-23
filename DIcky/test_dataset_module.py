# test_dataset_module.py
import unittest
from dataset_module import download_dataset, export_metadata


class TestDatasetModule(unittest.TestCase):
    # TC-31: Mengunduh dataset dengan metode default (download, csv)
    def test_download_default(self):
        result = download_dataset()
        self.assertIn("Dataset berhasil diunduh dengan semua metode", result)

    # TC-32: Mengunduh dataset menggunakan API
    def test_download_api(self):
        result = download_dataset(method="api")
        self.assertIn("Dataset berhasil diunduh via API", result)

    # TC-33: Mengunduh dataset dalam format ZIP
    def test_download_zip(self):
        result = download_dataset(method="download", format="zip")
        self.assertIn("File ZIP berhasil diunduh", result)

    # TC-34: Mengekspor metadata dataset
    def test_export_metadata(self):
        result = export_metadata()
        self.assertIn("Metadata dataset berhasil diekspor", result)


if __name__ == "__main__":
    unittest.main()
