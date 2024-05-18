from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from airflow.operators.postgres_operator import PostgresOperator  # type: ignore
import boto3
import os
from create_sql import json_to_sql      # type: ignore
from zip_files import zip_files         # type: ignore
from file_to_s3 import upload_file      # type: ignore

default_args = {
    'owner': 'John',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['jtamakloe6902@gmal.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Flightradar',
    default_args=default_args,
    description='Run Scrapy Spider',
    schedule_interval=timedelta(days=1),
)

scrape_task = BashOperator(
    task_id='scrape_task',
    bash_command='cd /opt/airflow/flight && scrapy crawl flight',
    dag=dag,
)



# Read the SQL file
sql_file_path = '/opt/airflow/sql/init.sql'
with open(sql_file_path, 'r') as file:
    sql_commands = file.read()

# Task to execute the SQL commands
execute_sql_file = PostgresOperator(
    task_id='execute_sql_file',
    postgres_conn_id='postgres_default',
    sql=sql_commands,
    dag=dag,
)

country_sql = PythonOperator(
    task_id="country_sql",
    python_callable=json_to_sql,
    op_kwargs = {
        'json_path':'/opt/airflow/flight/countries.json',
        'sql_path': '/opt/airflow/sql/countries.sql',
        'table_name': 'countries',
        'p_key':'code'
    },
    dag=dag,
)
airline_sql = PythonOperator(
    task_id="airline_sql",
    python_callable=json_to_sql,
    op_kwargs = {
        'json_path':'/opt/airflow/flight/airlines.json',
        'sql_path': '/opt/airflow/sql/airlines.sql',
        'table_name': 'airlines',
        'p_key':'code',
    },
    dag=dag,
)
airport_sql = PythonOperator(
    task_id="airport_sql",
    python_callable=json_to_sql,
    op_kwargs = {
        'json_path':'/opt/airflow/flight/airports.json',
        'sql_path': '/opt/airflow/sql/airports.sql',
        'table_name': 'airports',
        'p_key':'icao',
    },
    dag=dag,
)

zip_files_task = PythonOperator(
    task_id="zip_files_task",
    python_callable= zip_files,
    op_kwargs = {
         'file_paths': ['/opt/airflow/flight/airlines.json', '/opt/airflow/flight/airports.json', '/opt/airflow/flight/countries.json'], 
         'zip_path': '/opt/airflow/flight/flight_data.zip'
        },
    dag = dag,
)

s3_upload = PythonOperator(
    task_id="s3_upload",
    python_callable=upload_file,
    op_kwargs = {
        'file_name': '/opt/airflow/flight/flight_data.zip',
        'bucket': 'tbfirestagging',
        'object_name': 'flight_data.zip'
        },
    dag = dag,

)

# Read the SQL file
countries_sql_path = '/opt/airflow/sql/countries.sql'
with open(countries_sql_path, 'r') as file:
    sql_commands = file.read()

# Task to execute the SQL commands
insert_country_data = PostgresOperator(
    task_id='insert_country_data',
    postgres_conn_id='postgres_default',
    sql=sql_commands,
    dag=dag,
)
# Read the SQL file
airport_sql_path = '/opt/airflow/sql/airports.sql'
with open(airport_sql_path, 'r') as file:
    sql_commands = file.read()

# Task to execute the SQL commands
insert_airport_data = PostgresOperator(
    task_id='insert_airport_data',
    postgres_conn_id='postgres_default',
    sql=sql_commands,
    dag=dag,
)
# Read the SQL file
airline_sql_path = '/opt/airflow/sql/airlines.sql'
with open(airline_sql_path, 'r') as file:
    sql_commands = file.read()

# Task to execute the SQL commands
insert_airline_data = PostgresOperator(
    task_id='insert_airline_data',
    postgres_conn_id='postgres_default',
    sql=sql_commands,
    dag=dag,
)


scrape_task >> execute_sql_file >> [country_sql, airline_sql, airport_sql] >> insert_country_data >> insert_airport_data >> insert_airline_data
insert_country_data >> zip_files_task >> s3_upload
