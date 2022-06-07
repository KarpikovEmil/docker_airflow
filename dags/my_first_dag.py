from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import logging
import time

conn_id = 'PG_LOCAL'

args = dict(
    owner = 'pipis',
    start_date = days_ago(0, 0, 0, 0, 0),
    catchup = False,
    max_active_runs = 1,

)

def wait_5():
    time.sleep(300)

dag = DAG(dag_id='my_sample_dag', default_args=args, schedule_interval="*/5 * * * *", tags = ['test'])


with dag:
    run_this_task = PythonOperator(
        task_id="run_this_first",
        python_callable = wait_5

    )

    run_this_task
