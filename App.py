from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from src.db import Database
from src.controllers.member_controller import member_routes_bp
from src.controllers.payment_controller import payment_routes_bp
from src.controllers.activity_controller import activity_routes_bp
from src.utils.error_handlers import register_error_handlers

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def create_app():
    """Función de fábrica para crear la aplicación Flask."""
    app = Flask(__name__)

    # Habilitar CORS para permitir solicitudes desde cualquier dominio
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Cargar la configuración según el entorno
    env = os.getenv("FLASK_ENV", "development").lower()

    print(f"Ejecutando en modo {env}")

    # Seleccionar la configuración apropiada
    class_config = {
        "production": "config.ProductionConfig",
        "development": "config.DevelopmentConfig",
        "testing": "config.TestingConfig",
    }.get(env, "config.DevelopmentConfig")

    # Aplicar la configuración a la app
    app.config.from_object(class_config)

    # Inicializar la conexión con la base de datos
    app.db = Database(app.config)

    # Registrar manejadores de errores personalizados
    register_error_handlers(app)

    # Registrar las rutas mediante Blueprints
    app.register_blueprint(member_routes_bp)
    app.register_blueprint(payment_routes_bp)
    app.register_blueprint(activity_routes_bp)
    


    # Ruta principal para verificar que el servidor está activo
    @app.route("/")
    def home():
        return "¡Bienvenido a la API de Gestión del Gimnasio!"

    # Inicializar la base de datos al arrancar la aplicación
    with app.app_context():
        try:
            if app.db.test_connection():
                print("Conexión exitosa a la base de datos")
            else:
                print("Error al conectar con la base de datos")
        except Exception as e:
            print(f"Error al verificar la conexión: {e}")

    return app



if __name__ == "__main__":
    # Crear y ejecutar la aplicación
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
