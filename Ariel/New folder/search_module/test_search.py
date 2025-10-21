import unittest
from search import ModelSearchService

class TestModelSearchService(unittest.TestCase):

    def setUp(self):
        self.search_service = ModelSearchService()
        print(f"\nMenjalankan: {self.id()}")

    def test_TC40_filter_by_tag_valid(self):
        hasil = self.search_service.filter_by_tag("TensorFlow 2")
        self.assertEqual(len(hasil), 1, "Seharusnya menemukan 1 model dengan tag TensorFlow 2")
        self.assertIn("TensorFlow 2 Image Classifier", hasil)

    def test_TC40_filter_by_tag_tidak_ada(self):
        hasil = self.search_service.filter_by_tag("PyTorch")
        self.assertEqual(hasil, [], "Jika filter tidak ada di tag, harus mengembalikan list kosong")

    def test_TC40_filter_by_tag_case_insensitive(self):
        hasil = self.search_service.filter_by_tag("tensorFLOW 2")
        self.assertIn("TensorFlow 2 Image Classifier", hasil, "Filter seharusnya tidak peka huruf besar kecil")

    def test_TC41_1_search_keyword_valid_dan_spesifik(self):
        hasil = self.search_service.search_by_keyword("Titanic")
        self.assertEqual(len(hasil), 1, "Seharusnya menemukan 1 model")
        self.assertIn("Titanic Survival Prediction", hasil)

    def test_TC41_2_search_keyword_valid_dalam_tag(self):
        hasil = self.search_service.search_by_keyword("nlp")
        self.assertEqual(len(hasil), 1, "Seharusnya menemukan 1 model dari tag 'nlp'")
        self.assertIn("Sentiment Analysis with NLP", hasil)

    def test_TC41_3_search_keyword_umum(self):
        hasil = self.search_service.search_by_keyword("classification")
        self.assertEqual(len(hasil), 2, "Seharusnya menemukan 2 model dengan tag 'classification'")
        self.assertCountEqual(hasil, ["Titanic Survival Prediction", "Sentiment Analysis with NLP"])

    def test_TC41_4_search_keyword_tidak_ditemukan(self):
        hasil = self.search_service.search_by_keyword("quantum_computing_model")
        self.assertEqual(hasil, [], "Seharusnya mengembalikan list kosong jika model tidak ditemukan")

    def test_TC41_5_search_keyword_case_insensitive(self):
        hasil = self.search_service.search_by_keyword("rEgReSsIoN")
        self.assertEqual(len(hasil), 1, "Pencarian seharusnya case-insensitive")
        self.assertIn("House Prices: Advanced Regression", hasil)

    def test_TC41_6_search_dengan_input_kosong(self):
        hasil = self.search_service.search_by_keyword("")
        self.assertEqual(hasil, [], "Pencarian dengan keyword kosong seharusnya tidak mengembalikan hasil")

if __name__ == '__main__':
    unittest.main(verbosity=2)
