import unittest
from SearchDataset import SearchDataset
from dataset_module import download_dataset, export_metadata

class TestIntegrationMainFlow(unittest.TestCase):

    def test_main_integration_flow(self):
        """Integration Test: Search → Download → Export Metadata"""

        print("\n[STEP 1] Mencari dataset berdasarkan query...")
        searcher = SearchDataset()
        results = searcher.search(query="pendidikan")
        print("    Hasil pencarian:", results)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        print("[STEP 2] Mendownload dataset...")
        download_result = download_dataset()
        print("    Hasil download:", download_result)

        self.assertIn("Dataset berhasil diunduh", download_result)

        print("[STEP 3] Mengekspor metadata dataset...")
        metadata_result = export_metadata()
        print("    Hasil export:", metadata_result)

        self.assertIn("Metadata dataset berhasil diekspor", metadata_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
