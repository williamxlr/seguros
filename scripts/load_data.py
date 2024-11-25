import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, regexp_extract
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F  # Importar funciones como F
from pyspark.sql.types import StructType, StructField, StringType, DateType
import pymssql

# Inicializa la sesión de Spark
spark = SparkSession.builder.master("local").appName("DataCleaning").getOrCreate()

# Ruta del archivo cargado
file_path = "C:\\Users\\Usuario\\Documents\\WILLIAM\\DOCUMENTOS\\PERSONALES\\MONOKERA\\seguros\\MOCK_DATA.csv"

# Leer el archivo CSV y asegurarse de que tiene encabezado y tipo de datos inferido
data_3 = spark.read.csv(file_path, header=True, inferSchema=True)

# Verificar los nombres de las columnas
print("Column names: ", data_3.columns)

# Limpiar la columna 'id' para extraer solo los números (si están en el formato esperado)
data_3 = data_3.withColumn('id', regexp_extract(col('id'), r'\d+', 0))

# Filtrar filas donde 'id' no es nulo y contiene solo números
data_3_cleaned = data_3.filter(col('id').rlike('^\d+$'))

# Verificar si las columnas de fecha existen y convertirlas al formato correcto
date_columns = ["claim_date", "payment_date", "policy_start_date", "policy_end_date"]
for col_name in date_columns:
    if col_name in data_3_cleaned.columns:
        data_3_cleaned = data_3_cleaned.withColumn(col_name, to_date(col(col_name), "M/d/yyyy"))
    else:
        print(f"Columna '{col_name}' no encontrada")

# Manejo de valores nulos
# Rellenar valores nulos con valores predeterminados
data_cleaned = data_3_cleaned.fillna({
    "insured_age": 0,
    "insured_gender": "Unknown",
    "claim_status": "Unknown",
    "payment_status": "Unknown",
    "payment_method": "Unknown"
})

# Convertir columnas numéricas relevantes a tipos adecuados
numeric_columns = ["claim_amount", "payment_amount"]
for col_name in numeric_columns:
    if col_name in data_cleaned.columns:
        data_cleaned = data_cleaned.withColumn(col_name, col(col_name).cast(DoubleType()))
    else:
        print(f"Columna '{col_name}' no encontrada para conversión a tipo numérico")

# Filtrar y seleccionar las columnas necesarias para 'data_claim'
data_claim = data_cleaned.filter(F.col('claim_date').isNotNull()) \
    .select(
        F.col('policy_number').alias('id'),
        'claim_status',
        'claim_date',
        'claim_amount',
        'claim_description'
    )

# Agrupar por 'policy_number' y obtener los primeros valores de 'insured_name', 'insured_gender', 'insured_age', etc.
data_insured = data_cleaned.groupBy("policy_number").agg(
    F.first('insured_name').alias('insured_name'),
    F.first('insured_gender').alias('insured_gender'),
    F.first('insured_age').alias('insured_age'),
    F.first('insured_address').alias('insured_address'),
    F.first('insured_city').alias('insured_city'),
    F.first('insured_state').alias('insured_state'),
    F.first('insured_postal_code').alias('insured_postal_code'),
    F.first('insured_country').alias('insured_country')
).withColumnRenamed("policy_number", "id")

# Filtrar las columnas que contienen "payment" en su nombre
payment_columns = [col_name for col_name in data_cleaned.columns if "payment" in col_name]

# Crear el DataFrame con las columnas de payment y policy_number como id
data_payments = data_cleaned.select(
    F.col('policy_number').alias('id'),
    *payment_columns
)

# Filtrar filas donde payment_status sea diferente de 'Unknown'
data_payments_filtered = data_payments.filter(F.col('payment_status') != 'Unknown')

# Agrupar por 'policy_number' y obtener los primeros valores de 'premium_amount', 'deductible_amount', etc.
data_premium = data_cleaned.groupBy("policy_number").agg(
    F.first('premium_amount').alias('premium_amount'),
    F.first('deductible_amount').alias('deductible_amount'),
    F.first('coverage_limit').alias('coverage_limit')  
).withColumnRenamed("policy_number", "id")

# Agrupar por 'policy_number' y obtener los primeros valores de 'agent_name', 'agent_email', 'agent_phone'
data_agents = data_cleaned.groupBy("policy_number").agg(
    F.first('agent_name').alias('agent_name'),
    F.first('agent_email').alias('agent_email'),
    F.first('agent_phone').alias('agent_phone')
).withColumnRenamed("policy_number", "id")

# Filtrar para eliminar agentes con 'agent_name' nulo o 'Unknown'
data_agents_filtered = data_agents.filter(
    (F.col('agent_name').isNotNull()) & (F.col('agent_name') != 'Unknown')
)

# Convertir las fechas de las pólizas al formato adecuado
data_cleaned = data_cleaned.withColumn(
    'policy_start_date', to_date(col('policy_start_date'), 'yyyy-MM-dd')
).withColumn(
    'policy_end_date', to_date(col('policy_end_date'), 'yyyy-MM-dd')
)

# Manejo de valores nulos en fechas de pólizas (rellenar con una fecha predeterminada si es necesario)
data_cleaned = data_cleaned.fillna({
    "policy_start_date": "1900-01-01",
    "policy_end_date": "1900-01-01"
})

# Filtrar solo las columnas necesarias y crear el DataFrame 'data_policy'
data_policy = data_cleaned.select(
    col('policy_number'),
    col('policy_start_date'),
    col('policy_end_date'),
    col('policy_type'),
    col('insurance_company')
)

data_agents_filtered = data_agents_filtered.withColumnRenamed("id", "policy_number")
data_claim = data_claim.withColumnRenamed("id", "policy_number")
data_insured = data_insured.withColumnRenamed("id", "policy_number")
data_payments_filtered = data_payments_filtered.withColumnRenamed("id", "policy_number")
data_premium = data_premium.withColumnRenamed("id", "policy_number")
data_policy = data_policy.withColumnRenamed("id", "policy_number")

# Conectar a SQL Server utilizando pymssql
conn = pymssql.connect(
    server="LAPTOP-O07NV287",  # Dirección del servidor
    user="williamxlr",         # Nombre de usuario
    password="Al3xW$1978",     # Contraseña
    database="monokera"        # Nombre de la base de datos
)

cursor = conn.cursor()

# Función para cargar un DataFrame a la base de datos
def load_to_sql(df, table_name):
    try:
        for row in df.collect():
            query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
            cursor.execute(query, tuple(row))
        conn.commit()
        print(f"Datos cargados correctamente en la tabla {table_name}.")
    except Exception as e:
        print(f"Error al cargar datos en la tabla {table_name}: {e}")
        conn.rollback()

# Cargar DataFrames a las tablas de SQL Server (asegurándote de que las tablas ya están creadas)
load_to_sql(data_policy, 'policy')
load_to_sql(data_agents_filtered, 'agents')
load_to_sql(data_premium, 'premium')
load_to_sql(data_payments_filtered, 'payments')
load_to_sql(data_insured, 'insured')
load_to_sql(data_claim, 'claims')

# Cerrar la conexión
cursor.close()
conn.close()

print("Datos cargados correctamente en SQL Server.")
