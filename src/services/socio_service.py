from src.db import Database

class SocioService:
    @staticmethod
    def obtener_socios_activos():
        """Obtiene una lista de socios activos."""
        query = "SELECT * FROM socios WHERE estado = 'activo';"
        try:
            connection = Database.get_connection()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
            return resultados
        finally:
            connection.close()

    @staticmethod
    def registrar_socio(nombre, apellido, email, password):
        """Registra un nuevo socio en la base de datos."""
        query = """
        INSERT INTO socios (nombre, apellido, email, password)
        VALUES (%s, %s, %s, %s);
        """
        try:
            connection = Database.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, (nombre, apellido, email, password))
                connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()
