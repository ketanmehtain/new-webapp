# WebApp

This is demo app which need PostgreSQL DB connectivity. 

## How To Run App
Update *config.py* with PostgreSQL Flexible Server details on **AZURE_DB_CONFIG** and **DB_CONFIG** and not **GCP_DB_CONFIG**.

1. Install `virtualenv`:
    ```
    $ pip install virtualenv
    ```

2. Open a terminal in the project root directory and run:
    ```
    $ virtualenv env
    ```

3. Then run the command:
    ```
    $ .\env\Scripts\activate
    ```

4. Then install the dependencies:
    ```
    $ (env) pip install -r requirements.txt
    ```

5. Finally start the web server:
    ```
    $ (env) python app.py
    ```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

    ```python
    if __name__ == "__main__":
        app.run(debug=True, port=<desired port>)
    ```

## Migration

### Data Dump and Upload
On Azure

1. Take Database dump:
    ```
    $ (env) python migration.py dump
    ```

2. Upload data dump to Azure Blob Storage
    ```
    $ (env) python upload.py
    ```

### Data Transfer
Create Google Storage Transfer Job and copy data from Azure Blob Storage to GCS bucket.

### Data Download and Restore
On GCP
Update *config.py* with GCP PostgreSQL DB details on **GCP_DB_CONFIG** and **DB_CONFIG**.
Also update the **cred.json** with appropriate credential.

1.  Download Data from GCS Bucket
    ```
    $ (env) python download.py
    ```

2. Restore Data to PostgreSQL DB
    ```
    $ (env) python migration.py restore
    ```

## Run the App
*Follow the "How To Run App" to run the application. without chnaging **config.py***.