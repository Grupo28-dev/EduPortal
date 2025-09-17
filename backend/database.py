# database.py
import mysql.connector
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)  # Devuelve diccionarios en vez de tuplas
            print("Conexión a la base de datos exitosa.")
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            self.conn = None
            self.cursor = None

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def query(self, sql, params=None):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()  # Retorna todas las filas como diccionarios
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            return None

    def execute(self, sql, params=None):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            self.cursor.execute(sql, params)
            self.conn.commit()  # Confirma los cambios realizados
            return self.cursor.rowcount  # Devuelve el número de filas afectadas
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la operación: {err}")
            self.conn.rollback()  # Revierte los cambios si hay un error
            return 0
    def last_insert_id(self):
        if self.cursor:
            return self.cursor.lastrowid
        else:
            return None