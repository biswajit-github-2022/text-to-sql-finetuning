import pandas as pd
from sqlalchemy import create_engine
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
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



def query_to_csv(query, host, user, password, database, output_csv):
    if not query.strip():  # Check if the query is empty or just spaces
        print("Error: SQL query is empty. Please provide a valid query.")
        return

    # Create a connection string using SQLAlchemy
    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    
    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)
    
    # Execute the query and fetch the data into a DataFrame
    df = pd.read_sql_query(query, engine)
    
    # Save the result to a CSV file
    df.to_csv(output_csv, index=False)
    print("csv generated successsfully !!!")



# Example usage
host = "localhost" ##input
user = "root" ##input
password = "passwd" ##input
database = "movies" ##input

#collect schema from database
schema_ = get_database_schema(host, user, password, database)
print(f'"""\n{schema_}\n"""')

##import the model
model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

## specify the question and schema
question = "show how many data are there in the Reviews table " ##input
schema = f'"""\n{schema_}\n"""'

input_text = " ".join(["Question: ",question, "Schema:", schema])

## send the question and schema to the model
model_inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**model_inputs, max_length=512)
output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)

#show the output query 
print("SQL Query:")
print(output_text[0])


# Example usage
query = output_text[0]  # Replace this with a valid query like SELECT * FROM your_table_name
output_csv = "output_data.csv"  # Output CSV file name

query_to_csv(query,host, user, password, database, output_csv)

