# my_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import subprocess

# Define la función que ejecutará cada archivo .py
def run_cleardata():
    # Ejecuta el script cleardata.py
    subprocess.run(['python', r'C:\\Users\\Usuario\\Documents\\WILLIAM\\DOCUMENTOS\\PERSONALES\\MONOKERA\\scripts\\cleardata.py'], check=True)


def run_loaddata():
    # Ejecuta el script load_data.py
    subprocess.run(['python', r'C:\\Users\\Usuario\\Documents\\WILLIAM\\DOCUMENTOS\\PERSONALES\\MONOKERA\\scripts\\load_data.py'], check=True)

# Define los parámetros del DAG
dag = DAG(
    'data_processing_dag',  # Nombre del DAG
    description='DAG para limpiar y cargar datos',
    schedule_interval=None,  # Puedes configurar un cronograma si lo deseas
    start_date=datetime(2024, 11, 18),
    catchup=False,  # Evita ejecutar el DAG para fechas pasadas
)

# Define las tareas dentro del DAG
task_cleardata = PythonOperator(
    task_id='clear_data_task',  # Nombre de la tarea
    python_callable=run_cleardata,  # Función que se ejecutará
    dag=dag,
)

task_load_data = PythonOperator(
    task_id='load_data_task',
    python_callable=run_loaddata,
    dag=dag,
)

# Establece el orden de las tareas
task_cleardata >> task_load_data  # `cleardata` se ejecuta antes de `load_data`
