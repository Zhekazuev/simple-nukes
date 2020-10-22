"""
Simplifier MySQL methods
"""
import mysql.connector
import config


class MySQL:
    """
    Connection examples:
        1) without close() - 'with' statement
            with MySQL(host='1.1.1.1', database='database', username='user', password='pass') as sql:
                ...
        2) with close(close)
            sql = MySQL(host='1.1.1.1', database='database', username='user', password='pass')
            ...
            sql.close()

    Queries examples:
        1) Select one row
            with MySQL(host='1.1.1.1', database='database', username='user', password='pass') as sql:
                record = sql.select_one(f"SELECT * FROM table WHERE STATUS = 0")
                print(record)
        2) Select limit row
            with MySQL(host='1.1.1.1', database='database', username='user', password='pass') as sql:
                records = sql.select_size(f"SELECT * FROM table WHERE STATUS = 0", size=2)
                for record in records:
                    print(record)
        3) Select all
            with MySQL(host='1.1.1.1', database='database', username='user', password='pass') as sql:
                records = sql.select(f"SELECT * FROM table WHERE STATUS = 0")
                for record in records:
                    print(record)
        4) Insert, Update, Delete
    """
    def __init__(self, host=config.MySQL.host, database=config.MySQL.database, username=config.MySQL.username,
                 password=config.MySQL.password, connect_timeout=config.MySQL.connect_timeout):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connect_timeout = connect_timeout
        self.con = mysql.connector.connect(host=self.host, user=self.username, password=self.password,
                                           database=self.database, connect_timeout=self.connect_timeout)
        # remake response to dictionary
        self.cur = self.con.cursor(dictionary=True, buffered=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self.con

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    # def fetchall(self):
    #     return self.cursor.fetchall()

    # def fetchone(self):
    #     return self.cursor.fetchone()

    # def query(self, query, params=None):
    #     self.cursor.execute(query, params or ())
    #     return self.fetchall()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def select(self, query, params=None, ):
        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Failed to get record from table: {}".format(error))

    def select_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as error:
            print("Failed to get record from table: {}".format(error))

    def select_size(self, query, params=None, size=None):
        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchmany(size or ())
            return result
        except mysql.connector.Error as error:
            print("Failed to get record from table: {}".format(error))

    def update(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            print("Record Updated successfully ")
        except mysql.connector.Error as error:
            print("Failed to update record to database: {}".format(error))

    def insert(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            print("Record inserted successfully into Laptop table")
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

    def delete(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            print("Record inserted successfully into Laptop table")
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
