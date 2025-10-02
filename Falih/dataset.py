
def upload_dataset(file_format, file_size_mb=1, link=None, is_private=False):
    allowed_formats = ["csv", "zip", "json"]
    if file_format not in allowed_formats:
        return "Format tidak didukung"
    if file_size_mb > 100:  # contoh batas 100 MB
        return "File terlalu besar"
    if link:
        if is_private:
            return "Link tidak bisa diakses"
        return "Upload dari link sukses"
    return "Upload sukses"

def create_from_notebook():
    return "Dataset dari notebook berhasil"
