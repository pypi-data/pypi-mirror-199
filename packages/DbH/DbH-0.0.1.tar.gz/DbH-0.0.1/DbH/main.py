import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_string = ", ".join([f"{col[0]} {col[1]}" for col in columns])
        query = f"CREATE TABLE {table_name} ({columns_string})"
        self.cursor.execute(query)

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)

    def rename_table(self, old_name, new_name):
        query = f"ALTER TABLE {old_name} RENAME TO {new_name}"
        self.cursor.execute(query)

    def add_column(self, table_name, column_name, data_type):
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}"
        self.cursor.execute(query)

    def drop_column(self, table_name, column_name):
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        self.cursor.execute(query)

    def rename_column(self, table_name, old_name, new_name):
        query = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}"
        self.cursor.execute(query)

    def insert(self, table_name, data):
        keys = ", ".join(data.keys())
        values = ", ".join([f"'{val}'" for val in data.values()])
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
        self.cursor.execute(query)
        self.conn.commit()

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_where(self, table_name, condition):
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, data, condition):
        set_values = ", ".join(
            [f"{key}='{value}'" for key, value in data.items()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def delete(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def count(self, table_name, condition=None):
        if condition:
            query = f"SELECT COUNT(*) FROM {table_name} WHERE {condition}"
        else:
            query = f"SELECT COUNT(*) FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def max(self, table_name, column):
        query = f"SELECT MAX({column}) FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def min(self, table_name, column):
        query = f"SELECT MIN({column}) FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def group_by(self, table_name, group_column):
        query = f"SELECT {group_column}, COUNT(*) FROM {table_name} GROUP BY {group_column}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def join(self, table1, table2, join_column):
        query = f"SELECT * FROM {table1} INNER JOIN {table2} ON {table1}.{join_column} = {table2}.{join_column}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_index(self, table_name, column):
        query = f"CREATE INDEX idx_{table_name}_{column} ON {table_name}({column})"
        self.cursor.execute(query)

    def close(self):
        self.conn.close()
