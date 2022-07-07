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
    "pymongo[srv]",
    "tqdm",
    "recordlinkage"
]

requirements_venv = [
    "pandas",
    "bs4",
    "pymongo[srv]",
    "tqdm"
]

args={
    "owner": "Giang Vu  Long",
    "retries": 10,
    "start_date": days_ago(1)
}

with DAG(
    dag_id="etl",
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

    clean_data_task = PythonVirtualenvOperator(
        task_id="clean_data",
        requirements=requirements_venv,
        python_callable=clean_data
    )

    with TaskGroup(group_id="pair_matching") as tg2:
        mediamart_tgdd = PythonVirtualenvOperator(
            task_id="mediamart_tgdd",
            requirements=requirements,
            provide_context=True,
            system_site_packages=True,
            use_dill=True,
            python_callable=schema_matching,
            op_kwargs={'collection1': 'mediamart', 'collection2': 'thegioididong', 'matcher': 'jaccard'}
        )

        cellphones_didongthongminh = PythonVirtualenvOperator(
            task_id="cellphones_didongthongminh",
            requirements=requirements,
            provide_context=True,
            system_site_packages=True,
            use_dill=True,
            python_callable=schema_matching,
            op_kwargs={'collection1': 'cellphones', 'collection2': 'didongthongminh', 'matcher': 'jaccard'}
        )

    schema_matching_4 = PythonVirtualenvOperator(
        task_id="matching_four_source",
        requirements=requirements,
        provide_context=True,
        python_callable=schema_matching,
        system_site_packages=True,
        use_dill=True,
        op_kwargs={'collection1': 'cellphones_didongthongminh', 'collection2': 'mediamart_thegioididong', 'matcher': 'jaccard'}
    )

    schema_matching_5 = PythonVirtualenvOperator(
        task_id="matching_five_source",
        requirements=requirements,
        provide_context=True,
        system_site_packages=True,
        use_dill=True,
        python_callable=schema_matching,
        op_kwargs={'collection1': 'cellphones_didongthongminh_mediamart_thegioididong', 'collection2': 'phongvu',
                   'matcher': 'jaccard'}
    )

    data_matching_task = PythonVirtualenvOperator(
        task_id="data_matching",
        requirements=requirements,
        python_callable=data_matching
    )

    tg1 >> clean_data_task >> tg2 >> schema_matching_4 >> schema_matching_5 >> data_matching_task
