
# Dummy data forum
DISCUSSIONS = [
    {"id": 1, "title": "Belajar Deep Learning", "content": "Diskusi tentang CNN dan RNN", "tags": ["AI", "Deep Learning"], "filter": "Top"},
    {"id": 2, "title": "Pemula Machine Learning", "content": "Bagaimana memulai dengan Scikit-learn", "tags": ["AI", "ML"], "filter": "Newest"},
    {"id": 3, "title": "Tips Kaggle", "content": "Cara meningkatkan skor kompetisi Kaggle", "tags": ["Kaggle", "Competition"], "filter": "Top"},
    {"id": 4, "title": "Data Visualization", "content": "Diskusi matplotlib dan seaborn", "tags": ["Visualization"], "filter": "Newest"},
]

def comment_forum(text):
    return "Komentar berhasil" if text else "Komentar kosong"

def search_discussion(keyword=None, filter_by=None, tags=None):
    results = DISCUSSIONS

    if keyword:
        results = [d for d in results if keyword.lower() in d["title"].lower() or keyword.lower() in d["content"].lower()]
    if filter_by:
        results = [d for d in results if d["filter"].lower() == filter_by.lower()]
    if tags:
        results = [d for d in results if tags in d["tags"]]

    return results if results else []
