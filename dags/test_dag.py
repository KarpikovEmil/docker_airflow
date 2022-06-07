from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import logging
import time

conn_id = 'PG_LOCAL'

args = dict(
    owner = 'pipis',
    start_date = days_ago(0, 9, 0, 0, 0),
    catchup = False,
    max_active_runs = 1

)

def wait_5():
    time.sleep(10)

dag = DAG(dag_id='test_dag1', default_args=args, schedule_interval="*/1 * * * *", tags = ['test'])


with dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable = wait_5

    )

    task1