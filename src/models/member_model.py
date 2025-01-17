import mysql.connector
from datetime import datetime

class MemberModel:
    def __init__(self, db_connection):
        self.conn = db_connection

    def create_member(self, nombre, apellido, email, telefono, direccion, password):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO socios (nombre, apellido, email, telefono, direccion, password, fecha_registro, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'inactivo')
        """
        fecha_registro = datetime.utcnow()
        cursor.execute(query, (nombre, apellido, email, telefono, direccion, password, fecha_registro))
        self.conn.commit()
        return cursor.lastrowid

    def get_member_by_id(self, socio_id):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM socios WHERE id = %s"
        cursor.execute(query, (socio_id,))
        return cursor.fetchone()
