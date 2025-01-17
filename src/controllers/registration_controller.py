from flask import Blueprint, request, jsonify, current_app

registration_routes_bp = Blueprint("registration_routes", __name__, url_prefix="/inscripciones")

@registration_routes_bp.route("/", methods=["GET"])
def get_registrations():
    """Obtener la lista de inscripciones a actividades."""
    try:
        registrations = current_app.db.execute_query("SELECT * FROM inscripciones")
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@registration_routes_bp.route("/", methods=["POST"])
def register_activity():
    """Registrar a un socio en una actividad."""
    data = request.json
    query = """
    INSERT INTO inscripciones (socio_id, actividad_id, sesiones_restantes)
    VALUES (%s, %s, %s)
    """
    params = (data["socio_id"], data["actividad_id"], data.get("sesiones_restantes", 10))
    try:
        current_app.db.execute_update(query, params)
        return jsonify({"message": "Inscripción registrada exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
