from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

with DAG('daily_ricko',
    schedule_interval='0 0 * * *',
    start_date=datetime(2022, 7, 1)       
) as dag:

    start = DummyOperator(
        task_id='start'
    )    
      
    # orders

    ingest_orders = BashOperator(
        task_id='ingest_orders',
        bash_command="""python3 /root/airflow/dags/ingest/ricko/ingest_orders.py {{ execution_date.format('YYYY-MM-DD') }}"""
    )

    to_datalake_orders = BashOperator(
        task_id='to_datalake_orders',
        bash_command="""gsutil cp /root/output/ricko/orders/orders_{{ execution_date.format('YYYY-MM-DD') }}.csv gs://digitalskola-de-batch7/ricko/staging/orders/"""
    )

    # order_details

    ingest_order_details = BashOperator(
        task_id='ingest_order_details',
        bash_command="""python3 /root/airflow/dags/ingest/ricko/ingest_order_details.py {{ execution_date.format('YYYY-MM-DD') }}"""
    )

    to_datalake_order_details = BashOperator(
        task_id='to_datalake_order_details',
        bash_command="""gsutil cp /root/output/ricko/orders_detail/orders_detail_{{ execution_date.format('YYYY-MM-DD') }}.csv gs://digitalskola-de-batch7/ricko/staging/orders_detail/"""
    )

    # products

    ingest_products = BashOperator(
        task_id='ingest_products',
        bash_command="""python3 /root/airflow/dags/ingest/ricko/ingest_products.py {{ execution_date.format('YYYY-MM-DD') }}"""
    )

    to_datalake_products = BashOperator(
        task_id='to_datalake_products',
        bash_command="""gsutil cp /root/output/ricko/products/products_{{ execution_date.format('YYYY-MM-DD') }}.csv gs://digitalskola-de-batch7/ricko/staging/products/"""
    )

    # categories

    ingest_categories = BashOperator(
        task_id='ingest_categories',
        bash_command="""python3 /root/airflow/dags/ingest/ricko/ingest_categories.py {{ execution_date.format('YYYY-MM-DD') }}"""
    )

    to_datalake_categories = BashOperator(
        task_id='to_datalake_categories',
        bash_command="""gsutil cp /root/output/ricko/categories/categories_{{ execution_date.format('YYYY-MM-DD') }}.csv gs://digitalskola-de-batch7/ricko/staging/categories/"""
    )

    # suppliers

    ingest_suppliers = BashOperator(
        task_id='ingest_suppliers',
        bash_command="""python3 /root/airflow/dags/ingest/ricko/ingest_suppliers.py {{ execution_date.format('YYYY-MM-DD') }}"""
    )

    to_datalake_suppliers = BashOperator(
        task_id='to_datalake_suppliers',
        bash_command="""gsutil cp /root/output/ricko/suppliers/suppliers_{{ execution_date.format('YYYY-MM-DD') }}.csv gs://digitalskola-de-batch7/ricko/staging/suppliers/"""
    )

    start >> ingest_orders >> to_datalake_orders
    start >> ingest_order_details >> to_datalake_order_details
    start >> ingest_products >> to_datalake_products
    start >> ingest_categories >> to_datalake_categories
    start >> ingest_suppliers >> to_datalake_suppliers
