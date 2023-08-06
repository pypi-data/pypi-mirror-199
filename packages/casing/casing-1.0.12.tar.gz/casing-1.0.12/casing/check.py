import os

def file_integrity(path):
    if not os.path.isfile(path):
        raise Exception("file not found")
