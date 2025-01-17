import mysql.connector.pooling
import mysql.connector

class DbError(Exception):
    """Excepción personalizada para errores de la base de datos."""
    pass

class Database:
    def __init__(self, config):
        """Inicializa el pool de conexiones."""
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="pileta",
                pool_size=5,
                host=config['DB_HOST'],
                database=config['DB_NAME'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD']
            )

        except mysql.connector.Error as err:
            raise DbError(f"Error al conectar con la base de datos. {err.msg}")

    def get_connection(self):
        """Obtiene una conexión del pool."""
        try:
            return self.pool.get_connection()
        except mysql.connector.PoolError as err:
            raise DbError(f"Pool de conexiones agotada: {err.msg}")

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve los resultados.

        Args:
            query (str): La consulta SQL a ejecutar.
            params (tuple): Los parámetros de la consulta.

        Returns:
            list: Resultados de la consulta.
        """
        connection = self.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            raise DbError(f"Error ejecutando la consulta: {err.msg}")
        finally:
            cursor.close()
            connection.close()

    def execute_update(self, query, params=None):
        """
        Ejecuta una consulta SQL de tipo INSERT, UPDATE o DELETE.

        Args:
            query (str): La consulta SQL a ejecutar.
            params (tuple): Los parámetros de la consulta.

        Returns:
            int: Cantidad de filas afectadas.
        """
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            raise DbError(f"Error ejecutando la actualización: {err.msg}")
        finally:
            cursor.close()
            connection.close()
    def test_connection(self):
        """Prueba la conexión a la base de datos."""
        connection = self.get_connection()
        if connection.is_connected():
            connection.close()
            return True
        return False
