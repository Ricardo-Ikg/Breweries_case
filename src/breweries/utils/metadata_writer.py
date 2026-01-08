import json, os, hashlib
from datetime import datetime
from azure.storage.blob import BlobServiceClient

def write_bronze_metadata(records: int, ingestion_date: str, source_url: str):
    year, month, day = ingestion_date.split("-")

    metadata = {
        "source": source_url,
        "records": records,
        "ingestion_date": ingestion_date,
        "execution_time": datetime.now().isoformat(),
        "runtime_container": os.getenv("HOSTNAME", "local"),
        "status": "success"
    }

    metadata_path = (
        f"bronze/metadata/breweries/"
        f"year={year}/month={month}/day={day}/metadata.json"
    )

    connection = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={os.getenv('STORAGE_ACCOUNT')};"
        f"AccountKey={os.getenv('STORAGE_KEY')};"
        f"EndpointSuffix=core.windows.net"
    )
    blob = BlobServiceClient.from_connection_string(connection)
    blob_client = blob.get_blob_client(container="bronze", blob=metadata_path)
    blob_client.upload_blob(json.dumps(metadata, indent=2), overwrite=True)
