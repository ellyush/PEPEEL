import unittest
from search import ModelSearchService

class TestModelSearchService(unittest.TestCase):
    """
    Kelas ini berisi semua test case untuk memvalidasi fungsionalitas pencarian model.
    Setiap test case mewakili satu skenario dalam TC-41.
    """

    def setUp(self):
        """
        Metode ini dijalankan sebelum setiap metode test.
        Ini memastikan setiap test berjalan dengan instance service yang baru.
        """
        self.search_service = ModelSearchService()
        print(f"\nMenjalankan: {self.id()}")

    def test_TC41_1_search_keyword_valid_dan_spesifik(self):
        """TC-41.1: Mencari model dengan kata kunci valid yang cocok dengan satu nama model."""
        hasil = self.search_service.search_by_keyword("Titanic")
        self.assertEqual(len(hasil), 1, "Seharusnya menemukan 1 model")
        self.assertIn("Titanic Survival Prediction", hasil, "Nama model yang ditemukan tidak sesuai")

    def test_TC41_2_search_keyword_valid_dalam_tag(self):
        """TC-41.2: Mencari model dengan kata kunci valid yang cocok dengan tag."""
        hasil = self.search_service.search_by_keyword("nlp")
        self.assertEqual(len(hasil), 1, "Seharusnya menemukan 1 model dari tag 'nlp'")
        self.assertIn("Sentiment Analysis with NLP", hasil)

    def test_TC41_3_search_keyword_umum(self):
        """TC-41.3: Mencari model dengan kata kunci umum yang cocok dengan beberapa model."""
        hasil = self.search_service.search_by_keyword("classification")
        self.assertEqual(len(hasil), 2, "Seharusnya menemukan 2 model dengan tag 'classification'")
        # Menggunakan assertCountEqual karena urutan hasil tidak dijamin
        self.assertCountEqual(hasil, ["Titanic Survival Prediction", "Sentiment Analysis with NLP"])

    def test_TC41_4_search_keyword_tidak_ditemukan(self):
        """TC-41.4: Mencari model dengan kata kunci yang tidak ada di database."""
        hasil = self.search_service.search_by_keyword("quantum_computing_model")
        self.assertEqual(hasil, [], "Seharusnya mengembalikan list kosong jika model tidak ditemukan")

    def test_TC41_5_search_keyword_case_insensitive(self):
        """TC-41.5: Memastikan pencarian tidak membedakan huruf besar/kecil."""
        hasil = self.search_service.search_by_keyword("rEgReSsIoN")
        self.assertEqual(len(hasil), 1, "Pencarian seharusnya case-insensitive")
        self.assertIn("House Prices: Advanced Regression", hasil)

    def test_TC41_6_search_dengan_input_kosong(self):
        """TC-41.6: Memastikan pencarian dengan string kosong mengembalikan list kosong."""
        hasil = self.search_service.search_by_keyword("")
        self.assertEqual(hasil, [], "Pencarian dengan keyword kosong seharusnya tidak mengembalikan hasil")

# Baris ini memungkinkan script test dijalankan langsung dari terminal
if __name__ == '__main__':
    unittest.main(verbosity=2)