FROM apache/airflow:2.9.3-python3.12

USER root

RUN mkdir -p /opt/airflow/data/bronze \
             /opt/airflow/data/silver \
             /opt/airflow/data/gold \
    && chown -R airflow:0 /opt/airflow/data

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
