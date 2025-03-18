import os
from google.cloud import storage

# Set path to service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\azureuser\\new-webapp\\cred.json"

# Define variables
bucket_name = "pg-replication-bucket-lloyds"
source_blob_name = "test/backup.sql"
destination_file_path = "C:\\Users\\azureuser\\new-webapp\\backup.sql"

# Initialize a GCS client
client = storage.Client()

# Get the bucket and blob
bucket = client.bucket(bucket_name)
blob = bucket.blob(source_blob_name)

# Download the file
try:
    blob.download_to_filename(destination_file_path)
    print(f"File downloaded successfully to {destination_file_path}")
except Exception as e:
    print(f"Error downloading file: {e}")