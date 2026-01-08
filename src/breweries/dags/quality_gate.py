def decide_gold_execution_logic(metadata: dict) -> str:
    status = metadata.get("status")

    if status == "success":
        return "gold"

    return "skip_gold"