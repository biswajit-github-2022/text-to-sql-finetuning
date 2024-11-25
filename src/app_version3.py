import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pymysql

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


finetuned_model = AutoModelForSeq2SeqLM.from_pretrained("weights")
# finetuned_model = finetuned_model.to('cuda')


# Function to fetch the database schema
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
        st.error(f"Error: {e}")
    finally:
        connection.close()
    
    return " ".join(schema_output)


# Function to execute a query and fetch data into a DataFrame
def query_to_dataframe(query, host, user, password, database):
    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)
    try:
        return pd.read_sql_query(query, engine)
    except Exception as e:
        st.error(f"Error executing the query: {e}")
        return None

def schema_to_dict_with_create(schema):
    # Split the schema into individual table definitions
    tables = schema.split("[SEP]")
    schema_dict = {}
    
    for table in tables:
        table = table.strip()
        if not table:
            continue
        
        # Extract the table name and schema
        parts = table.split(" ", 1)
        table_name = parts[0].strip('"')
        table_schema = parts[1].strip() if len(parts) > 1 else ""
        
        # Build the CREATE TABLE statement
        create_table_statement = f'CREATE TABLE {table_name} (\n{table_schema}\n);'
        
        # Store in dictionary with table name as key
        schema_dict[table_name] = create_table_statement
    
    return schema_dict

# Input schema











# Streamlit UI
st.title("SQL Query Generator and Executor")

# Input fields
host = st.text_input("Host")
user = st.text_input("UserName")
password = st.text_input("Password", type="password")
database = st.text_input("Database")
table_name=st.text_input("Table Name")
question = st.text_area("Enter your natural language question:")

if st.button("Generate SQL Query"):
    if not host or not user or not password or not database or not question:
        st.error("Please fill in all the fields.")
    else:
        # Fetch schema
        schema = get_database_schema(host, user, password, database)
        st.text_area("Schema", schema, height=200)
        # Input schema

        # Convert schema to dictionary
        schema_dict = schema_to_dict_with_create(schema)

        # Example: Retrieve CREATE TABLE statement by table name
    
        if table_name in schema_dict:
            # print(f"CREATE TABLE statement for '{table_name}':\n{schema_dict[table_name]}")
            print(schema_dict[table_name])
            formatted_schema = schema_dict[table_name]
        else:
            print(f"Table '{table_name}' not found.")
        # Load the model
        # model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
        # model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        # tokenizer = AutoTokenizer.from_pretrained(model_path)


        prompt = f"""Tables:
        {formatted_schema}

        Question:
        {question}

        Answer:
        """


        model_name='t5-small'

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        inputs = tokenizer(prompt, return_tensors='pt')
        # inputs = inputs.to('cuda')

        output = tokenizer.decode(
            finetuned_model.generate(
                inputs["input_ids"], 
                max_new_tokens=200,
            )[0], 
            skip_special_tokens=True
        )


        # Generate SQL query
        # input_text = " ".join(["Question:", question, "Schema:", schema])
        # model_inputs = tokenizer(input_text, return_tensors="pt")
        # outputs = model.generate(**model_inputs, max_length=512)
        # output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        sql_query = output+';'
        st.subheader("Generated SQL Query")
        st.code(sql_query)

        print(sql_query)
        # Execute query and display results
        result_df = query_to_dataframe(sql_query, host, user, password, database)
        if result_df is not None:
            st.subheader("Query Results")
            st.dataframe(result_df)

