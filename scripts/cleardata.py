import pymssql

# Conectar a SQL Server utilizando pymssql
conn = pymssql.connect(
    server="LAPTOP-O07NV287",  # Dirección del servidor
    user="williamxlr",         # Nombre de usuario
    password="Al3xW$1978",     # Contraseña
    database="monokera"        # Nombre de la base de datos
)

cursor = conn.cursor()

# Función para eliminar los datos de las tablas
def delete_rows():
    try:
        # Deshabilitar las restricciones de claves foráneas en todas las tablas
        cursor.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT all'")
        print("Restricciones de claves foráneas deshabilitadas.")

        # Definir las tablas que deseas limpiar
        tables_to_delete_from = [
            'agents',
            'premium',
            'payments',
            'insured',
            'claims',
            'policy',  # Asegúrate de incluir esta tabla
        ]
        
        # Ejecutar DELETE para cada tabla
        for table in tables_to_delete_from:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Datos de la tabla {table} eliminados correctamente.")
        
        # Confirmar los cambios en la base de datos
        conn.commit()

        # Habilitar nuevamente las restricciones de claves foráneas
        cursor.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? CHECK CONSTRAINT all'")
        print("Restricciones de claves foráneas habilitadas.")

    except Exception as e:
        print(f"Error al eliminar los datos de las tablas: {e}")
        conn.rollback()

# Llamar a la función para eliminar los datos
delete_rows()

# Cerrar la conexión
cursor.close()
conn.close()

print("Datos eliminados correctamente en SQL Server.")
