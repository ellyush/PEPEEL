from search_dataset import SearchDataset
from dataset_module import download_dataset


class SearchDownloadIntegration:
    def __init__(self):
        self.search_module = SearchDataset()
        self.last_search_result = None
        self.selected_dataset_id = None

    def search_model(self, query="", tag="", fltr=""):
        result = self.search_module.search(query=query, tag=tag, fltr=fltr)
        self.last_search_result = result

        if isinstance(result, list) and len(result) > 0:
            self.selected_dataset_id = result[0]["id"]
            return result
        else:
            self.selected_dataset_id = None
            return result

    def download_model(self, method="download", format="csv"):
        if not self.selected_dataset_id:
            return "Tidak ada dataset yang dipilih untuk diunduh"

        return download_dataset(method=method, format=format)
