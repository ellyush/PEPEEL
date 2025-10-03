class ModelSearchService:
    """
    Kelas layanan untuk mensimulasikan pencarian model di Kaggle.
    """
    def __init__(self):
        """
        Inisialisasi dengan database dummy yang berisi beberapa model.
        Setiap model memiliki nama dan tag untuk disimulasikan dalam pencarian.
        """
        self._database_model = [
            {
                "nama": "Titanic Survival Prediction",
                "author": "Kaggle Team",
                "tags": ["classification", "tabular", "beginner"]
            },
            {
                "nama": "House Prices: Advanced Regression",
                "author": "Jane Doe",
                "tags": ["regression", "housing", "xgboost"]
            },
            {
                "nama": "Sentiment Analysis with NLP",
                "author": "John Smith",
                "tags": ["nlp", "text", "classification"]
            },
            {
                "nama": "Image Recognition CNN",
                "author": "AI Corp",
                "tags": ["computer vision", "cnn", "images"]
            }
        ]

    def search_by_keyword(self, keyword):
        """
        Mencari model yang namanya atau tag-nya mengandung kata kunci.
        Pencarian ini tidak case-sensitive (tidak membedakan huruf besar/kecil).
        """
        if not keyword or not isinstance(keyword, str):
            return [] # Mengembalikan list kosong jika keyword tidak valid

        hasil_pencarian = []
        keyword_lower = keyword.lower()

        for model in self._database_model:
            # Cek apakah keyword ada di dalam nama model
            if keyword_lower in model["nama"].lower():
                hasil_pencarian.append(model["nama"])
                continue # Lanjut ke model berikutnya agar tidak ada duplikat

            # Jika tidak ada di nama, cek di dalam setiap tag
            for tag in model["tags"]:
                if keyword_lower in tag.lower():
                    hasil_pencarian.append(model["nama"])
                    break # Hentikan loop tag jika sudah ditemukan, lanjut ke model berikutnya
        
        return hasil_pencarian