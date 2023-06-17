# airflow-dbt-metabase

This repository provides a Docker Compose setup for running Airflow, dbt, and Metabase together.

## Prerequisites

- Docker
- Docker Compose
- Poetry

## Getting Started

Follow the steps below to set up and run the project.

1. Clone the repository:

   ```shell
   git clone https://github.com/alfredosa/airflow-dbt-metabase.git
   cd airflow-dbt-metabase
   ```

2. Install project dependencies using Poetry:

  ```shell
  pip install poetry # if you are missing poetry
  poetry install
  ```

3. Create a `.env` file and provide the necessary environment variables. An example is provided in

  ```shell
  cp .env.example .env
  ```

Additionally, you can customize other environment variables based on your requirements.

4. Start the application using Docker Compose:

  ```shell
  docker-compose up -d
  ```
This will build and start the required containers defined in the `docker-compose.yml` file.

5a. Medium guide for this repo:

https://medium.com/@asuarezaceves/streamlined-data-pipelines-orchestrating-dbt-transformations-with-airflow-and-cosmos-visualizing-85a200ffb6df

5. Access Airflow:

Open your browser and visit [http://localhost:8080](http://localhost:8080) to access the Airflow UI.

Run the pipeline pokemon_dbt_dag.py!

6. Access Metabase:

Open your browser and visit [http://localhost:3030](http://localhost:3000) to access the Metabase UI.



## Additional Information

- Docker Compose: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- Poetry: [https://python-poetry.org/](https://python-poetry.org/)
- Cosmos: [https://github.com/astronomer/astronomer-cosmos](https://github.com/astronomer/astronomer-cosmos)
## License

Specify the license for your project.
