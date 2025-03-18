import requests

# Define variables
file_path = "C:\\Users\\azureuser\\new-webapp\\backup.sql"
blob_name = "backup.sql"

# Construct the Blob Storage URL
blob_uri = f""

# Upload the file to Blob Storage
try:
    print(f"Uploading {file_path} to {blob_uri}")
    headers = {"x-ms-blob-type": "BlockBlob"}
    
    with open(file_path, "rb") as file_data:
        response = requests.put(blob_uri, headers=headers, data=file_data)
    
    if response.status_code in [200, 201]:
        print("File uploaded successfully!")
    else:
        print(f"Error uploading file: {response.text}")
except Exception as e:
    print(f"Error uploading file: {e}")