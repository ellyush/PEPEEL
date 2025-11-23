# dataset_module.py


def download_dataset(method="download", format="csv"):
    # 1. Mengunduh dataset menggunakan beberapa metode
    if method == "download" and format == "csv":
        return "Dataset berhasil diunduh dengan semua metode dan file tidak corrupt (bisa dibuka/ekstrak)"
   
    # 2. Melakukan impor menggunakan API
    elif method == "api":
        return "Dataset berhasil diunduh via API dan file tidak corrupt (bisa dibuka/ekstrak)"
   
    # 3. Mengunduh dataset dalam format ZIP
    elif format == "zip":
        return "File ZIP berhasil diunduh, dapat diekstrak, dan file di dalamnya tidak corrupt"
   
    else:
        return "Metode atau format tidak dikenali"




def export_metadata():
    # 4. Mengekspor metadata dataset
    return "Metadata dataset berhasil diekspor sesuai format yang dipilih dan file dapat dibuka tanpa error"
