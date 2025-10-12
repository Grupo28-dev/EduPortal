
import mysql.connector
from config import DB_CONFIG


class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None

    def connect(self):
        try:
            self._conn = mysql.connector.connect(**DB_CONFIG)
            self._cursor = self._conn.cursor(dictionary=True)
            print("Conexión a la base de datos exitosa.")
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            self._conn = None
            self._cursor = None

    def disconnect(self):
        if self._conn and self._conn.is_connected():
            self._cursor.close()
            self._conn.close()
            print("Conexión a la base de datos cerrada.")

    def _ensure(self):
        if not self._conn or not self._conn.is_connected():
            self.connect()

    def query(self, sql, params=None):
        try:
            self._ensure()
            self._cursor.execute(sql, params)
            return self._cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            return None

    def execute(self, sql, params=None):
        try:
            self._ensure()
            self._cursor.execute(sql, params)
            self._conn.commit()
            return self._cursor.rowcount
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la operación: {err}")
            self._conn.rollback()
            return 0

    def last_insert_id(self):
        if self._cursor:
            return self._cursor.lastrowid
        return None
