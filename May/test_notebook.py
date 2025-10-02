import unittest
from notebook import Notebook

class TestKaggleNotebook(unittest.TestCase):
    def setUp(self):
        self.nb = Notebook()  

    # TC-54: Membuat notebook baru
    def test_TC54_create_notebook(self):
        self.assertTrue(self.nb.create_notebook("My Notebook"))

    # TC-55: Mengubah nama notebook
    def test_TC55_rename_notebook(self):
        self.nb.create_notebook("Old")
        self.assertEqual(self.nb.rename_notebook("New"), "New")

    # TC-56: Mengubah jenis accelerator (misal CPU/GPU/TPU)
    def test_TC56_change_accelerator(self):
        self.assertEqual(self.nb.change_accelerator("GPU"), "GPU")

    # TC-57: Menambah, menghapus, dan memindahkan sel
    def test_TC57_add_delete_move_cell(self):
        self.nb.add_cell("print('a')")
        self.nb.add_cell("print('b')")
        self.assertEqual(len(self.nb.cells), 2)
        self.nb.move_cell(0, 1)
        self.assertEqual(len(self.nb.cells), 2)
        self.nb.delete_cell(0)
        self.assertEqual(len(self.nb.cells), 1)

    # TC-58: Menggabungkan dan memisahkan sel
    def test_TC58_merge_split_cells(self):
        self.nb.add_cell("print('a');print('b')")
        self.nb.split_cell(0, ";")
        self.assertGreater(len(self.nb.cells), 1)
        self.nb.merge_cells(0, 1)
        self.assertEqual(len(self.nb.cells), 1)

    # TC-59: Mengunggah dataset lokal
    def test_TC59_upload_dataset(self):
        self.assertEqual(self.nb.upload_dataset("local.csv"), "local.csv")

    # TC-60: Menambahkan dataset dari Kaggle
    def test_TC60_add_kaggle_dataset(self):
        self.assertEqual(self.nb.add_kaggle_dataset("dataset123"), "dataset123")

    # TC-61: Menginstal library
    def test_TC61_install_library(self):
        self.assertEqual(self.nb.install_library("pandas"), "pandas installed")

    # TC-62: Menjalankan satu sel
    def test_TC62_run_cell(self):
        self.nb.add_cell("x=5")
        result = self.nb.run_cell(0)
        self.assertIn("Executed", result)

    # TC-63: Menjalankan semua sel
    def test_TC63_run_all(self):
        self.nb.add_cell("x=1")
        self.nb.add_cell("y=2")
        result = self.nb.run_all()
        self.assertEqual(len(result), 2)

    # TC-64: Visualisasi data
    def test_TC64_visualize_data(self):
        self.assertIn("Visualization", self.nb.visualize_data([1,2,3]))

    # TC-65: Restart session notebook
    def test_TC65_restart_session(self):
        self.nb.add_cell("x=1")
        self.assertTrue(self.nb.restart_session())
        self.assertEqual(len(self.nb.cells), 0)

    # TC-66: Menyimpan versi notebook
    def test_TC66_save_version(self):
        self.nb.save_version()
        self.assertEqual(self.nb.save_version(), 2)

    # TC-67: Mengubah privasi notebook
    def test_TC67_change_privacy(self):
        self.assertEqual(self.nb.change_privacy("Public"), "Public")

    # TC-68: Menjadwalkan run notebook
    def test_TC68_schedule_run(self):
        self.assertTrue(self.nb.schedule_run())

    # TC-69: Mengunduh notebook
    def test_TC69_download_notebook(self):
        self.nb.create_notebook("MyNB")
        self.assertEqual(self.nb.download_notebook(), "MyNB.ipynb")

    # TC-70: Menghapus notebook
    def test_TC70_delete_notebook(self):
        self.assertTrue(self.nb.delete_notebook())

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)

