import unittest
from model_download import ModelDownloadService

class TestModelDownloaderService(unittest.TestCase):

    def setUp(self):
        self.download_service = ModelDownloadService()
        print(f"\nMenjalankan: {self.id()}")

    def test_TC42_import_model_via_kaggle_api(self):
        """TC-42: Menguji impor model machine learning menggunakan Kaggle API."""
        model_path = "google/gemma/2b"
        hasil = self.download_service.download_with_kaggle_api(model_path)
        self.assertIn(f"Model '{model_path}' berhasil diunduh", hasil)

    def test_TC42_import_model_via_kaggle_api_gagal(self):
        """TC-42 (Negative): Menguji impor model yang tidak ada menggunakan Kaggle API."""
        model_path = "non/existent/model"
        hasil = self.download_service.download_with_kaggle_api(model_path)
        self.assertIn("Error: Model", hasil)

    def test_TC43_import_model_via_kagglehub(self):
        """TC-43: Menguji impor model machine learning menggunakan KaggleHub."""
        model_path = "meta/llama2/7b"
        hasil = self.download_service.download_with_kagglehub(model_path)
        self.assertIn(f"Model '{model_path}' berhasil diunduh ke path:", hasil)

    def test_TC44_import_model_via_curl(self):
        """TC-44: Menguji impor model machine learning menggunakan cURL."""
        # Link diambil dari database dummy di service
        download_link = "https://kaggle.com/models/google/gemma/2b/download"
        hasil = self.download_service.download_with_curl(download_link)
        self.assertEqual(hasil, "File 'model.zip' berhasil diunduh.")

    def test_TC44_import_model_via_curl_link_salah(self):
        """TC-44 (Negative): Menguji impor model menggunakan link cURL yang salah."""
        download_link = "https://example.com/invalid-link"
        hasil = self.download_service.download_with_curl(download_link)
        self.assertIn("Error: Link unduhan tidak valid", hasil)

    def test_TC45_download_model_as_targz(self):
        """TC-45: Menguji unduhan model machine learning dengan format tar.gz."""
        model_path = "google/gemma/2b"
        hasil = self.download_service.download_with_specific_format(model_path, file_format="tar.gz")
        self.assertEqual(hasil, f"Model '{model_path}' berhasil diunduh dalam format 'tar.gz'.")

    def test_TC45_download_model_default_format_zip(self):
        """TC-45 (Default): Menguji unduhan model dengan format default (zip)."""
        model_path = "meta/llama2/7b"
        hasil = self.download_service.download_with_specific_format(model_path) # Tanpa argumen format
        self.assertEqual(hasil, f"Model '{model_path}' berhasil diunduh dalam format 'zip'.")


# Baris ini memungkinkan script test dijalankan langsung dari terminal
if __name__ == '__main__':
    unittest.main(verbosity=2)