import os
import json
import csv
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
        print(create_table_query)
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
            table_name = os.path.splitext(filename)[0]
            if not table_exists(table_name):
                schema_path = os.path.join(schemas_folder, filename)
                with open(schema_path, 'r') as schema_file:
                    table_schema = json.load(schema_file)
                    create_table_from_schema(table_name, table_schema)

def table_exists(table_name):
    try:
        db_connector.connect()
        query = f"SELECT table_name FROM information_schema.tables WHERE table_name = %s"
        result = db_connector.execute_query(query, (table_name,))
        return bool(result)
    finally:
        db_connector.disconnect()

def insert_data_from_csvs():
    init_data_folder = os.path.join(os.path.dirname(__file__), 'init_data')
    for filename in os.listdir(init_data_folder):
        if filename.endswith('.csv'):
            table_name = os.path.splitext(filename)[0]
            if table_exists(table_name):
                csv_path = os.path.join(init_data_folder, filename)
                db_connector.copy_from_csv(table_name, csv_path)

@app.route('/api/data')
def get_data():
    try:
        db_connector.connect()
        result = db_connector.execute_query("SELECT * FROM test_data")
        return jsonify(result)
    finally:
        db_connector.disconnect()

if __name__ == '__main__':
    wait_for_database()
    check_and_create_tables_from_schemas()
    insert_data_from_csvs()
    app.run(host='0.0.0.0', port=5150)