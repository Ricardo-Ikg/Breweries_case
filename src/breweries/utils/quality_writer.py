import json
from pathlib import Path
from datetime import datetime


def write_quality_errors(
    *,
    layer: str,
    dataset: str,
    execution_date: str,
    error: str,
    base_path: str = "data/quality"
) -> None:
    year, month, day = execution_date.split("-")

    output_path = (
        Path(base_path)
        / layer
        / dataset
        / f"year={year}"
        / f"month={month}"
        / f"day={day}"
    )

    output_path.mkdir(parents=True, exist_ok=True)

    payload = {
        "layer": layer,
        "dataset": dataset,
        "execution_date": execution_date,
        "error": error,
        "created_at": datetime.utcnow().isoformat(),
    }

    with open(output_path / "quality_errors.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
