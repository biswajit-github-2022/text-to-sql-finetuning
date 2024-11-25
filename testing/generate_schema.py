import pymysql

def get_database_schema(host, user, password, database):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    schema_output = []
    
    try:
        with connection.cursor() as cursor:
            # Get all table names in the database
            cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database}';")
            tables = cursor.fetchall()
            
            for (table_name,) in tables:
                table_schema = []
                primary_keys = []
                
                # Get column details for each table
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, COLUMN_KEY
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table_name}';
                """)
                columns = cursor.fetchall()
                
                for column_name, data_type, column_key in columns:
                    table_schema.append(f'"{column_name}" {data_type}')
                    if column_key == "PRI":
                        primary_keys.append(f'"{column_name}"')
                
                # Combine table schema and primary key details
                primary_keys_str = f'primary key: {",".join(primary_keys)}' if primary_keys else ""
                schema_output.append(f'"{table_name}" {", ".join(table_schema)} {primary_keys_str} [SEP]')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
    
    # Join all table schemas
    return " ".join(schema_output)

# Example usage
host = "localhost"
user = "root"
password = "passwd"
database = "movies"

schema = get_database_schema(host, user, password, database)
print(f'"""\n{schema}\n"""')

