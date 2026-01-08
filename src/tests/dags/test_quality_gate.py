from breweries.dags.quality_gate import decide_gold_execution_logic
import pytest

@pytest.mark.dag
def test_gold_runs_when_silver_success():
    metadata = {"status": "success"}
    assert decide_gold_execution_logic(metadata) == "gold"

@pytest.mark.dag
def test_gold_skipped_when_quality_failed():
    metadata = {"status": "quality_failed"}
    assert decide_gold_execution_logic(metadata) == "skip_gold"

@pytest.mark.dag
def test_gold_skipped_when_status_missing():
    metadata = {}
    assert decide_gold_execution_logic(metadata) == "skip_gold"
