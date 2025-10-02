# test_competition.py
import unittest
from Kompetisi import Competition


class TestCompetition(unittest.TestCase):
    def setUp(self):
        self.comp = Competition("AI Challenge", max_submission=2)

    def test_submit_file(self):
        result = self.comp.submit_result("dummy file", "file")
        self.assertIn("Sistem berhasil menangkap file", result)

    def test_submit_api(self):
        result = self.comp.submit_result("dummy file", "api")
        self.assertIn("Sistem berhasil menangkap api", result)

    def test_submit_multi_limit(self):
        # sudah dipakai 2 kali di atas, coba sekali lagi
        self.comp.submit_result("f1", "file")
        self.comp.submit_result("f2", "file")
        result = self.comp.submit_result("f3", "file")
        self.assertIn("Sistem menanggulangi multi submission", result)

    def test_submit_notebook(self):
        comp = Competition("Notebook Challenge")
        result = comp.submit_result("nb", "notebook")
        self.assertIn("Sistem berhasil menangkap notebook", result)

    def test_download(self):
        result = self.comp.download_data()
        self.assertIn("Data relevan dengan kompetisi", result)

    def test_add_collection(self):
        result = self.comp.add_to_collection("dataset1")
        self.assertIn("Kompetisi dimasukkan ke dalam koleksi", result)

    def test_search_by_tag(self):
        result = self.comp.search_discussion(tag="machine-learning")
        self.assertTrue(isinstance(result, list) or "Menampilkan kompetisi yang memiliki tag" in result)

    def test_search_by_filter(self):
        result = self.comp.search_discussion(filter="recent")
        self.assertTrue(isinstance(result, list) or "Menampilkan kompitisi dengan filter" in result)


if __name__ == "__main__":
    unittest.main()
