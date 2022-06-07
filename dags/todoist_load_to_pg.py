"""
Save info from Todoist to PG
"""
from pathlib import Path
from typing import Any, Dict
import time
import json
import requests as re
import logging

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

DAG_FILE = Path(__file__)

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
json_str = """[ { "id": 2266101084, "color": 48, "name": "Inbox", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "inbox_project": true, "url": "https://todoist.com/showProject?id=2266101084" }, { "id": 2266102370, "order": 1, "color": 31, "name": "Работа", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2266102370" }, { "id": 2281199547, "order": 2, "color": 46, "name": "Проекты", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2281199547" }, { "id": 2276172551, "order": 3, "color": 41, "name": "Финансы", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2276172551" }, { "id": 2275765087, "order": 4, "color": 33, "name": "Организационно-бытовые задачи", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275765087" }, { "id": 2275777802, "order": 5, "color": 36, "name": "Красота и здоровье", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275777802" }, { "id": 2275765259, "order": 6, "color": 37, "name": "Личная эффективность", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275765259" }, { "id": 2286290517, "order": 7, "color": 34, "name": "Soft", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2286290517" }, { "id": 2276173208, "order": 8, "color": 30, "name": "Семья", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2276173208" }, { "id": 2281200101, "order": 9, "color": 35, "name": "Друзья", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2281200101" } ]"""
table_str = "table"


def generate_sql(table_str, json_str):

    json_object = json.loads(json_str)
    keys = list(json_object[0].keys())
    logging.info(f"{keys}, ключи")

    substr_list = []

    for obj in json_object:
        sub_list = []
        sub_string = "(" + ",".join(sub_list) + ")"
        for key in keys:
            sub_list.append(obj[key])
        substr_list.append(sub_string)
    sql_str = f"insert into {table_str} values" + ",".join(substr_list) + ";"
    logging.info(f"{sql_str}, sql")
    return sql_str


def create_dag(dag_args: Dict[str, Any]) -> DAG:
    with DAG(**dag_args) as result:
        task_api_active = HttpSensor(
            task_id='task_api_active',
            http_conn_id='todo_conn',
            method='GET',
            endpoint='/projects'
        )
        task_get_proj = SimpleHttpOperator(
            task_id='task_get_proj',
            http_conn_id='todo_conn',
            endpoint='/projects',
            method='GET',
            log_response=True
        )
        task_generate_sql = PythonOperator(
            task_id='generate_sql',
            python_callable=generate_sql,
            op_args=[table_str, json_str]

        )
    task_api_active >> task_get_proj >> task_generate_sql
    return result


dag = create_dag(DAG_ARGS)
