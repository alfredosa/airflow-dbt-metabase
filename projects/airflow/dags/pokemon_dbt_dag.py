import pandas as pd
import requests
from airflow import DAG
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from cosmos.providers.dbt.task_group import DbtTaskGroup

with DAG(
    "pokemons_dbt_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    def flatten_stats(data):
        columns = set()
        flattened_data = []

        for pokemon in data:
            base_columns = ["name", "order", "base_experience", "height", "weight"]
            columns = set()
            stats = pokemon.pop("stats", [])

            for stat in stats:
                column = stat["stat"]["name"]
                value = stat["base_stat"]

                columns.add(column)
                pokemon[column] = value

            flattened_data.append(pokemon)
        final_columns = base_columns + list(columns)
        return flattened_data, final_columns

    def extract(**context) -> list:
        url = "http://pokeapi.co/api/v2/pokemon"
        params = {"limit": 200}
        response = requests.get(url=url, params=params)

        json_response = response.json()
        results = json_response["results"]

        pokemons = [requests.get(url=result["url"]).json() for result in results]
        return pokemons

    def transform(pokemons: list):
        flattened_data, columns = flatten_stats(pokemons)
        df = pd.DataFrame(data=flattened_data, columns=columns)
        df = df.sort_values(["base_experience"], ascending=False)
        transformed_data = df.to_dict("records")
        return transformed_data

    def load(**context):
        transformed_data = context["ti"].xcom_pull(task_ids="transform")
        columns = transformed_data[0].keys()

        hook = PostgresHook(postgres_conn_id="postgres")
        conn = hook.get_conn()

        cursor = conn.cursor()

        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS pokemons (
                name TEXT,
                {', '.join(f'"{column}" INT' for column in columns if column != 'name')}
            )
        """
        cursor.execute(create_table_query)
        conn.commit()

        insert_query = f"""
            INSERT INTO pokemons ({', '.join(f'"{column}"' for column in columns)})
            VALUES ({', '.join(['%s'] * len(columns))})
        """

        values = [[item[column] for column in columns] for item in transformed_data]
        cursor.executemany(insert_query, values)
        conn.commit()

        cursor.close()
        conn.close()

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
        op_kwargs={"pokemons": extract_task.output},
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    dbt_task = DbtTaskGroup(
        dbt_root_path="/opt/airflow/dbt",
        dbt_project_name="airflowdbt",
        conn_id="postgres",
        profile_args={
            "schema": "public",
        },
    )

    end_pipeline = EmptyOperator(task_id="post_dbt")

    extract_task >> transform_task >> load_task >> dbt_task >> end_pipeline
