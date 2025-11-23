import unittest
from SearchDataset import SearchDataset

class TestSearchDataset(unittest.TestCase):
    def setUp(self):
        self.search = SearchDataset()

    # 1. TC-22 Mencari dataset berdasarkan tags
    def test_search_by_tag(self):
        result = self.search.search(tag="kampus")
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]["title"], "Data Mahasiswa") # type: ignore

    # 2. TC-23 Mengganti params GET di URI menjadi tag lain (valid)
    def test_replace_tag_valid(self):
        result = self.search.search(tag="ekonomi")
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]["title"], "Data Penjualan") # type: ignore

    # 3. TC-24 Mengganti params GET di URI menjadi tag lain (non-valid)
    def test_replace_tag_invalid(self):
        result = self.search.search(tag="xyz")
        self.assertEqual(result, "Tidak ada dataset ditemukan")

    # 4. TC-25 Mencari dataset berdasarkan filter
    def test_search_by_filter(self):
        result = self.search.search(fltr="public")
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]["filter"], "public") # type: ignore

    # 5. TC-26 Menggunakan filter tidak valid
    def test_invalid_filter(self):
        result = self.search.search(fltr="invalid")
        self.assertEqual(result, "Filter tidak valid")

    # 6. TC-27 Filter dengan value tidak biasa
    def test_unusual_filter(self):
        result = self.search.search(fltr="!@#$%")
        self.assertEqual(result, "Filter tidak valid")

    # 7. TC-28 Mencari dataset dengan mengetikkan kata
    def test_search_by_keyword(self):
        result = self.search.search(query="Kesehatan")
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]["title"], "Data Kesehatan") # type: ignore

    # 8. TC-29 Mencari dataset menggunakan kata kunci karakter khusus
    def test_search_special_chars(self):
        result = self.search.search(query="@@@")
        self.assertEqual(result, "Tidak ada dataset ditemukan")

    # 9. TC-30 Mencari dataset menggunakan kata kunci karakter random
    def test_search_random_word(self):
        result = self.search.search(query="asdfghjkl")
        self.assertEqual(result, "Tidak ada dataset ditemukan")


if __name__ == "__main__":
    unittest.main()
