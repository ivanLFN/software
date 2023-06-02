import psycopg2


class DatabaseConnection():
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",  # Адрес сервера базы данных
            port="7777",  # Порт сервера базы данных
            database="avax_db",  # Имя базы данных
            user="ivan",  # Имя пользователя
            password="ivan"  # Пароль пользователя
        )

        self.create_table()


    def create_table(self):
        cursor = self.conn.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS data_table (
                id SERIAL PRIMARY KEY,
                value TEXT
            )
        '''
        cursor.execute(create_table_query)
        self.conn.commit()
        cursor.close()

    def insert_data(self, value):
        cursor = self.conn.cursor()

        insert_query = '''
            INSERT INTO data_table (value)
            VALUES (%s)
        '''
        data = (value,)
        cursor.execute(insert_query, data)
        self.conn.commit()
        cursor.close()

    def fetch_data(self):
        cursor = self.conn.cursor()

        select_query = "SELECT * FROM data_table"
        cursor.execute(select_query)

        rows = cursor.fetchall()
        for row in rows:
            id_value = row[0]  # Значение поля id
            value = row[1]  # Значение поля value
            print(f"ID: {id_value}, Value: {value}")

        cursor.close()

    def close_connection(self):
        self.conn.close()


