from flask import Blueprint, request, jsonify, current_app

member_routes_bp = Blueprint("member_routes", __name__, url_prefix="/socios")

@member_routes_bp.route("/", methods=["GET"])
def get_socios():
    """Obtener la lista de todos los socios."""
    try:
        socios = current_app.db.execute_query("SELECT * FROM socios")
        return jsonify(socios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@member_routes_bp.route("/", methods=["POST"])
def add_socio():
    """Agregar un nuevo socio."""
    data = request.json
    query = """
    INSERT INTO socios (nombre, apellido, email, telefono, direccion)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (data["nombre"], data["apellido"], data["email"], data.get("telefono"), data.get("direccion"))
    try:
        current_app.db.execute_update(query, params)
        return jsonify({"message": "Socio agregado exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@member_routes_bp.route("/<int:socio_id>", methods=["GET"])
def get_socio(socio_id):
    """Obtener los detalles de un socio específico por su ID."""
    try:
        query = "SELECT * FROM socios WHERE id = %s"
        params = (socio_id,)
        socio = current_app.db.execute_query(query, params)
        
        if not socio:
            return jsonify({"message": "Socio no encontrado."}), 404
        
        return jsonify(socio[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500