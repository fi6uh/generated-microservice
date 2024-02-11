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

def check_and_create_test_data_table():
    try:
        wait_for_database()  # Wait until the database is online before proceeding
        db_connector.connect()
        result = db_connector.execute_query("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'test_data')")
        table_exists = result[0][0]

        if not table_exists:
            # Create the table with a basic example schema
            schema = {
                'id': 'SERIAL PRIMARY KEY',
                'name': 'VARCHAR(255)',
                'age': 'INTEGER'
            }
            db_connector.create_table('test_data', schema)
    finally:
        db_connector.disconnect()

@app.route('/api/data')
def get_data():
    try:
        db_connector.connect()
        # Assuming you already have data in the "test_data" table
        result = db_connector.execute_query("SELECT * FROM test_data")
        return jsonify(result)
    finally:
        db_connector.disconnect()

if __name__ == '__main__':
    check_and_create_test_data_table()  # Call this function to check and create the table before running the application
    app.run(host='0.0.0.0', port=5150)