import os

from google.cloud import storage

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return blob


def make_blob_public(blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(blob_name)

    blob.make_public()
    return blob


def upload_public_blob(zipf_path, blob_name):
    blob = upload_blob(zipf_path, blob_name)
    blob.make_public()
    return blob
