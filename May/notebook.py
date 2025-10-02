class Notebook:
    def __init__(self):
        self.name = None
        self.cells = []
        self.accelerator = "CPU"
        self.saved_versions = 0
        self.datasets = []
        self.privacy = "Private"
        self.scheduled = False
        self.deleted = False

    def create_notebook(self, name):  # TC-54
        self.name = name
        return True

    def rename_notebook(self, new_name):  # TC-55
        self.name = new_name
        return self.name

    def change_accelerator(self, acc):  # TC-56
        self.accelerator = acc
        return self.accelerator

    def add_cell(self, code):  # TC-57
        self.cells.append(code)

    def delete_cell(self, index):  # TC-57
        if 0 <= index < len(self.cells):
            del self.cells[index]
            return True
        return False

    def move_cell(self, from_idx, to_idx):  # TC-57
        if 0 <= from_idx < len(self.cells) and 0 <= to_idx < len(self.cells):
            cell = self.cells.pop(from_idx)
            self.cells.insert(to_idx, cell)
            return True
        return False

    def merge_cells(self, idx1, idx2):  # TC-58
        if idx1 < len(self.cells) and idx2 < len(self.cells):
            self.cells[idx1] += " " + self.cells[idx2]
            del self.cells[idx2]
            return True
        return False

    def split_cell(self, index, delimiter=";"):  # TC-58
        if 0 <= index < len(self.cells):
            parts = self.cells[index].split(delimiter)
            self.cells[index] = parts[0]
            self.cells.extend(parts[1:])
            return True
        return False

    def upload_dataset(self, dataset_name):  # TC-59
        self.datasets.append(dataset_name)
        return dataset_name

    def add_kaggle_dataset(self, dataset_name):  # TC-60
        self.datasets.append(f"kaggle:{dataset_name}")
        return dataset_name

    def install_library(self, lib_name):  # TC-61
        return f"{lib_name} installed"

    def run_cell(self, index):  # TC-62
        if 0 <= index < len(self.cells):
            return f"Executed: {self.cells[index]}"
        return None

    def run_all(self):  # TC-63
        return [f"Executed: {c}" for c in self.cells]

    def visualize_data(self, data):  # TC-64
        return f"Visualization of {len(data)} items"

    def restart_session(self):  # TC-65
        self.cells = []
        self.datasets = []
        return True

    def save_version(self):  # TC-66
        self.saved_versions += 1
        return self.saved_versions

    def change_privacy(self, privacy):  # TC-67
        if privacy in ["Public", "Private"]:
            self.privacy = privacy
            return self.privacy
        return None

    def schedule_run(self):  # TC-68
        self.scheduled = True
        return self.scheduled

    def download_notebook(self):  # TC-69
        return f"{self.name}.ipynb" if self.name else None

    def delete_notebook(self):  # TC-70
        self.deleted = True
        return self.deleted
