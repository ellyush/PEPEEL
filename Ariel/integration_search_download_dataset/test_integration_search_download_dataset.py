# test_integration_search_download.py

import unittest
from integration_search_download_dataset import SearchDownloadIntegration


class TestIntegrationSearchDownload(unittest.TestCase):

    def setUp(self):
        self.sys = SearchDownloadIntegration()

    # TC-IT-003 — Cari then Download
    def test_search_then_download(self):
        # Step 1: Search
        search_result = self.sys.search_model(query="Data")
        self.assertIsInstance(search_result, list)
        self.assertIsNotNone(self.sys.selected_dataset_id)

        # Step 2: Download
        download_result = self.sys.download_model(method="download", format="csv")
        self.assertIn("berhasil diunduh", download_result)

    # Negative: Search gagal → Download gagal
    def test_download_without_search(self):
        result = self.sys.download_model()
        self.assertEqual(result, "Tidak ada dataset yang dipilih untuk diunduh")

    # Cari berdasarkan tag → ID harus terisi → download berhasil
    def test_search_by_tag_then_download(self):
        search_result = self.sys.search_model(tag="medis")
        self.assertIsInstance(search_result, list)
        self.assertEqual(search_result[0]["title"], "Data Kesehatan")

        download_result = self.sys.download_model(method="api")
        self.assertIn("berhasil diunduh", download_result)

    # Cari dengan filter salah → Download tidak boleh jalan
    def test_invalid_filter_then_download(self):
        search_result = self.sys.search_model(fltr="private")
        self.assertEqual(search_result, "Filter tidak valid")
        self.assertIsNone(self.sys.selected_dataset_id)

        download_result = self.sys.download_model()
        self.assertEqual(download_result, "Tidak ada dataset yang dipilih untuk diunduh")


if __name__ == "__main__":
    unittest.main()
