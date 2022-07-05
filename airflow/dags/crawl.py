import os
import sys
import pendulum

sys.path.append(os.path.realpath(
    os.path.join(__file__, os.pardir)
))
sys.path.append("/opt/airflow/dags")

from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonVirtualenvOperator
from operators import *
#from operator.utils import *

requirements=[
    "pandas",
    "valentine"
]

requirements_venv = [
    "pandas",
    "bs4",
    "pymongo[srv]"
]

args={
    "owner": "Giang Vu  Long",
    "retries": 10,
    "start_date": days_ago(1)
}

with DAG(
    dag_id="crawl",
    catchup=False,
    tags=["crawl"],
    default_args=args,
    schedule_interval="@daily"
) as dag:
    with TaskGroup(group_id="crawl") as tg1:
        mediamart_task = PythonVirtualenvOperator(
            task_id="mediamart",
            requirements=requirements_venv,
            python_callable=crawl_mediaMart
        )

        thegioididong_task = PythonVirtualenvOperator(
            task_id="thegioididong",
            requirements=requirements_venv,
            python_callable=crawlTGDD
        )

        cellphones_task = PythonVirtualenvOperator(
            task_id="cellphones",
            requirements=requirements_venv,
            python_callable=crawlCellphones
        )

        didongthongminh = PythonVirtualenvOperator(
            task_id="didongthongminh",
            requirements=requirements_venv,
            python_callable=crawlDDTM
        )

        phongvu = PythonVirtualenvOperator(
            task_id="phongvu",
            requirements=requirements_venv,
            python_callable=crawlPhongVu
        )

    # clean_task = PythonVirtualenvOperator(
    #     task_id="clean",
    #     requirements=requirements,
    #     python_callable=clean_data
    # )

    # schema_matching = PythonVirtualenvOperator(
    #     task_id="schema_matching",
    #     requiremennts=requirements,
    #     pythonn_callable=schema_matching
    # )

    tg1
