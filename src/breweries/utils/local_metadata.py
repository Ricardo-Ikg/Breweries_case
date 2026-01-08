import json
from pathlib import Path
from datetime import datetime


def write_metadata(
    *,
    ingestion_date: str,
    source: str,
    status: str,
    layer: str,
    dataset: str,
    payload: dict | None,
    partitions: dict | None = None,
    base_path: str = "data",
    error: str | None = None,
) -> None:
    
    path = Path(base_path) / layer / dataset

    if partitions:
        for key, value in partitions.items():
            path = path / f"{key}={value}"
    path.mkdir(parents=True, exist_ok=True)

    metadata = {
        "ingestion_date": ingestion_date,
        "source": source,
        "status": status,
        "layer": layer,
        "dataset": dataset,
        "partition": partitions,
        "payload": payload,
        "error": error,
        "created_at": datetime.utcnow().isoformat(),
    }

    with open(path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
