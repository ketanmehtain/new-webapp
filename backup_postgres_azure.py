import os
import subprocess
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from config import DB_CONFIG, AZURE_STORAGE_CONFIG

# Generate dump file name with timestamp
backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

# PostgreSQL dump command
dump_command = f"PGPASSWORD={DB_CONFIG['password']} pg_dump -h {DB_CONFIG['host']} -p {DB_CONFIG['port']} -U {DB_CONFIG['user']} -F c -b -v -f {backup_file} {DB_CONFIG['dbname']}"

try:
    # Run the dump command
    subprocess.run(dump_command, shell=True, check=True)
    print(f"Database dump successful: {backup_file}")
except subprocess.CalledProcessError as e:
    print(f"Error dumping database: {e}")
    exit(1)

# Azure Blob Storage Connection String
connection_string = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_CONFIG['account_name']};AccountKey={AZURE_STORAGE_CONFIG['account_key']};EndpointSuffix=core.windows.net"

# Upload to Azure Blob Storage
try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONFIG['container_name'], blob=backup_file)

    with open(backup_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Backup uploaded to Azure Blob Storage: {backup_file}")

except Exception as e:
    print(f"Error uploading to Azure Blob Storage: {e}")

# Cleanup local dump file
os.remove(backup_file)
print(f"Local backup file deleted: {backup_file}")