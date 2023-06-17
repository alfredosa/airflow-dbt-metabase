FROM apache/airflow:latest-python3.10

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential gcc python3-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
COPY ./projects/airflow/requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
