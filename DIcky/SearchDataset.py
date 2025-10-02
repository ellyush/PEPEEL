from typing import List, Dict

class SearchDataset:
    def __init__(self):
        # data dummy
        self.data: List[Dict[str, str | list[str]]] = [
            {"id": "1", "title": "Data Mahasiswa", "tags": ["pendidikan", "kampus"], "filter": "public"},
            {"id": "2", "title": "Data Penjualan", "tags": ["ekonomi", "dagang"], "filter": "restricted"},
            {"id": "3", "title": "Data Kesehatan", "tags": ["medis", "rumah sakit"], "filter": "public"},
        ]

    def search(self, query: str = "", tag: str = "", fltr: str = ""):
        # 1. Cari berdasarkan tag
        if tag:
            results = [d for d in self.data if tag in d["tags"]]
            if results:
                return results
            return "Tidak ada dataset ditemukan"

        # 2. Cari berdasarkan filter
        if fltr:
            if fltr not in ["public", "restricted"]:
                return "Filter tidak valid"
            results = [d for d in self.data if d["filter"] == fltr]
            if results:
                return results
            return "Tidak ada dataset ditemukan"

        # 3. Cari berdasarkan query (kata kunci)
        if query:
            results = [d for d in self.data if query.lower() in str(d["title"]).lower()]
            if results:
                return results
            return "Tidak ada dataset ditemukan"

        # default jika tidak ada input
        return "Tidak ada dataset ditemukan"
