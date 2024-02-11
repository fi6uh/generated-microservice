import psycopg2

class DatabaseConnector:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to the database.")
        except psycopg2.Error as e:
            print(f"Error: Unable to connect to the database. {e}")
            raise

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print(f"Error: Unable to execute query. {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def format_columns(self, schema):
        """
        Format the schema dictionary into a list of tuples.

        Args:
        - schema (dict): A dictionary representing the table schema where keys are column names and values are data types.

        Returns:
        - list: A list of tuples representing the columns in the format (column_name, data_type).
        """
        return [(col, schema[col]) for col in schema]

    def create_table(self, table_name, schema):
        """
        Create a new table in the database.

        Args:
        - table_name (str): The name of the new table.
        - schema (dict): A dictionary representing the table schema where keys are column names and values are data types.

        Example:
        schema = {
            'id': 'SERIAL PRIMARY KEY',
            'name': 'VARCHAR(255)',
            'age': 'INTEGER'
        }
        db_connector.create_table('example_table', schema)
        """
        try:
            with self.connection.cursor() as cursor:
                columns = self.format_columns(schema)
                # Construct the CREATE TABLE SQL statement
                sql = f"CREATE TABLE {table_name} ({', '.join([f'{col[0]} {col[1]}' for col in columns])})"
                cursor.execute(sql)
                self.connection.commit()
                print(f"Table '{table_name}' created successfully.")
        except psycopg2.Error as e:
            print(f"Error: Unable to create table. {e}")
            raise
