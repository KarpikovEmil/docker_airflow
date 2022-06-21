"""
Save info from Todoist to PG
"""
from pathlib import Path
from typing import Any, Dict
import datetime
import json
import pandas as pd
import requests as re
import logging
from sqlalchemy import create_engine

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

DAG_FILE = Path(__file__)

pg_con = 'PG_LOCAL'

DAG_ARGS = dict(
    dag_id=DAG_FILE.name.rsplit(".", 1)[0],
    schedule_interval="00 00 * * *",
    start_date=days_ago(1),
    max_active_runs=1,
    tags=['todoist'],
    default_args=dict(
        owner='emil',

    )
)

end_points =['projects', 'sections', 'tasks', 'labels']

def json_to_df(table_name, schema_name, **kwargs):

    # Получение данных для втавки
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids=f'task_get_{table_name}')
    json_object = json.loads(data)
    df = pd.json_normalize(json_object)
    df['dag_run'] = datetime.datetime.now()
    logging.info(f'{df}')

    # Создание коннекшена
    postgres_hook = PostgresHook(postgres_conn_id = pg_con)
    engine = postgres_hook.get_sqlalchemy_engine()

    # Вставка данных
    df.to_sql(name = table_name, con = engine, schema= schema_name, index = False, if_exists='append')



def create_dag(dag_args: Dict[str, Any]) -> DAG:
    with DAG(**dag_args) as result:

        for i in end_points:
            task_api_active = HttpSensor(
                task_id=f'task_api_active_{i}',
                http_conn_id='todo_conn',
                method='GET',
                endpoint=i
            )
            task_get_proj = SimpleHttpOperator(
                task_id=f'task_get_{i}',
                http_conn_id='todo_conn',
                endpoint=i,
                method='GET',
                log_response=True
            )
            task_json_to_df = PythonOperator(
                task_id=f'json_to_df_{i}',
                python_callable=json_to_df,
                op_args=[i, 'stage']

            )
            task_api_active >> task_get_proj >> task_json_to_df
    return result


dag = create_dag(DAG_ARGS)
