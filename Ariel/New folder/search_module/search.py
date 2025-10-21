class ModelSearchService:
    def __init__(self):
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
            },
            {
                "nama": "TensorFlow 2 Image Classifier",
                "author": "DeepAI",
                "tags": ["tensorflow 2", "cnn", "deep learning"]
            }
        ]

    def search_by_keyword(self, keyword):
        if not keyword or not isinstance(keyword, str):
            return []

        hasil_pencarian = []
        keyword_lower = keyword.lower()

        for model in self._database_model:
            if keyword_lower in model["nama"].lower():
                hasil_pencarian.append(model["nama"])
                continue

            for tag in model["tags"]:
                if keyword_lower in tag.lower():
                    hasil_pencarian.append(model["nama"])
                    break
        
        return hasil_pencarian

    # === Tambahan untuk TC-40 ===
    def filter_by_tag(self, filter_tag):
        """Mengembalikan model yang memiliki tag sesuai filter."""
        if not filter_tag or not isinstance(filter_tag, str):
            return []
        filter_lower = filter_tag.lower()
        hasil_filter = [
            model["nama"]
            for model in self._database_model
            if any(filter_lower in tag.lower() for tag in model["tags"])
        ]
        return hasil_filter
