from pathlib import Path
import json


def save_to_local(
    *,
    data: list,
    year: str,
    month: str,
    day: str,
    base_path: str
) -> str:
    output_dir = (
        Path(base_path)
        / f"year={year}"
        / f"month={month}"
        / f"day={day}"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "breweries.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return str(output_file)
