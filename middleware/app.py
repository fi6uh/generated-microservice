import os
import json
from flask import Flask, jsonify
from database_connector import DatabaseConnector
import retrying

app = Flask(__name__)


db_connector = DatabaseConnector(
    host='172.18.0.4',
    port=5432,
    database='mydatabase',
    user='myuser',
    password='mypassword'
)

# Function to wait for the database to be online
@retrying.retry(wait_fixed=1000, stop_max_delay=10000)
def wait_for_database():
    db_connector.connect()
    db_connector.disconnect()

def create_table_from_schema(table_name, schema):
    try:
        db_connector.connect()
        formatted_schema = format_schema_for_db(schema)
        create_table_query = f"CREATE TABLE {table_name} ({formatted_schema})"
        db_connector.execute_query(create_table_query)
    finally:
        db_connector.disconnect()

def format_schema_for_db(schema):
    # Convert the schema dictionary to a string that can be used in a CREATE TABLE query
    formatted_schema = ', '.join([f'{column} {datatype}' for column, datatype in schema.items()])
    return formatted_schema

def check_and_create_tables_from_schemas():
    schemas_folder = os.path.join(os.path.dirname(__file__), 'schemas')
    for filename in os.listdir(schemas_folder):
        if filename.endswith('.json'):
            schema_path = os.path.join(schemas_folder, filename)
            with open(schema_path, 'r') as schema_file:
                schema_data = json.load(schema_file)
                table_name = schema_data.get('table_name')
                table_schema = schema_data.get('schema')
                if table_name and table_schema:
                    if not table_exists(table_name):
                        create_table_from_schema(table_name, table_schema)

def table_exists(table_name):
    try:
        db_connector.connect()
        result = db_connector.execute_query(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
        return result[0][0]
    finally:
        db_connector.disconnect()

@app.route('/api/data')
def get_data():
    try:
        db_connector.connect()
        result = db_connector.execute_query("SELECT * FROM test_data")
        return jsonify(result)
    finally:
        db_connector.disconnect()

if __name__ == '__main__':
    check_and_create_test_data_table()  # Call this function to check and create the table before running the application
    app.run(host='0.0.0.0', port=5150)