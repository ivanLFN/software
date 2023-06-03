import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port="7777",
            database="avax_db",
            user="ivan",
            password="ivan"
        )
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS study_table (
                id SERIAL PRIMARY KEY,
                title TEXT,
                position TEXT,
                created_at TEXT,
                description TEXT
            )
        '''

        cursor.execute(create_table_query)
        self.conn.commit()
        cursor.close()

    def fetch_all_data(self):
        cursor = self.conn.cursor()

        select_query = "SELECT * FROM study_table"
        cursor.execute(select_query)

        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()

        return list(rows)

    def insert_data(self, title, position, created_at, description):
        cursor = self.conn.cursor()

        insert_query = '''
            INSERT INTO study_table (title, position, created_at, description)
            VALUES (%s, %s, %s, %s)
        '''

        data = (title, position, created_at, description)
        cursor.execute(insert_query, data)
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        self.conn.close()