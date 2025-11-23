# competition.py

class Competition:
    def __init__(self, name, max_submission=3):
        self.name = name
        self.max_submission = max_submission
        self.submission_count = 0
        self.collection = []
        # dummy diskusi
        self.discussions = [
            {"title": "Diskusi optimasi model", "tag": "machine-learning", "filter": "popular"},
            {"title": "Diskusi data cleaning", "tag": "data-prep", "filter": "recent"},
        ]

    def submit_result(self, file_text, method):
        if self.submission_count >= self.max_submission:
            return "Sistem menanggulangi multi submission, menyesuaikan jika bisa multisubmission atau tidaknya"

        self.submission_count += 1
        if method in ["file", "api", "notebook"]:
            return f"Sistem berhasil menangkap {method} dan {method} disubmit ke penyelenggara kompetisi"
        return "Metode submit tidak valid"

    def download_data(self):
        return f"Data relevan dengan kompetisi {self.name} dapat didownload di device pengguna"

    def add_to_collection(self, dataset_text):
        self.collection.append(dataset_text)
        return "Kompetisi dimasukkan ke dalam koleksi kompetisi yang dibuat untuk pengkategorian"

    def search_discussion(self, query="", tag="", filter=""):
        # cari berdasarkan tag
        if tag:
            results = [d for d in self.discussions if d["tag"] == tag]
            return results if results else "Menampilkan kompetisi yang memiliki tag yang sesuai"

        # cari berdasarkan filter
        if filter:
            results = [d for d in self.discussions if d["filter"] == filter]
            return results if results else "Menampilkan kompitisi dengan filter yang sesuai dengan inputan"

        return "Tidak ada diskusi ditemukan"
