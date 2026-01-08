from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

from breweries.utils.read_local import list_silver_countries

BASE_CMD = "export PYTHONPATH=/opt/airflow/src && python /opt/airflow/src/breweries"


with DAG(
    dag_id="breweries_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["breweries", "pandas", "data-quality"],
) as dag:


    bronze = BashOperator(
        task_id="bronze",
        bash_command="""
        export PYTHONPATH=/opt/airflow/src && \
        python /opt/airflow/src/breweries/bronze/ingestion.py \
        https://api.openbrewerydb.org/v1/breweries \
        {{ ds }}
        """,
    )


    silver = BashOperator(
        task_id="silver",
        bash_command="""
        export PYTHONPATH=/opt/airflow/src && \
        python /opt/airflow/src/breweries/silver/silver_breweries.py \
        /opt/airflow/data/bronze/breweries \
        /opt/airflow/data/silver/breweries \
        {{ ds }}
        """,
    )


    @task
    def list_countries() -> list[str]:
        return list_silver_countries(
            dataset="breweries",
            base_path="/opt/airflow/data",
        )

    @task.branch
    def decide_gold(countries: list[str]) -> str:
        if countries:
            return "run_gold"
        return "skip_gold"

    
    run_gold = BashOperator(
    task_id="run_gold",
    bash_command="""
    export PYTHONPATH=/opt/airflow/src && \
    python /opt/airflow/src/breweries/gold/gold_breweries.py \
    /opt/airflow/data/silver/breweries \
    /opt/airflow/data/gold/breweries \
    {{ ds }}
    """,
)


    skip_gold = EmptyOperator(
        task_id="skip_gold",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )


    countries = list_countries()
    decision = decide_gold(countries)

    bronze >> silver >> countries >> decision
    decision >> run_gold
    decision >> skip_gold
