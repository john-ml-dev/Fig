import zipfile

def zip_files(file_paths, zip_path):
    """
    Zips multiple specified files.

    :param file_paths: List of paths to the files to be zipped
    :param zip_path: Path where the zip file will be created
    """
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(file_path, arcname=file_path.split('/')[-1])
