from flask import Blueprint, request, jsonify, current_app

attendance_routes_bp = Blueprint("attendance_routes", __name__, url_prefix="/asistencias")

@attendance_routes_bp.route("/", methods=["GET"])
def get_attendances():
    """Obtener la lista de asistencias."""
    try:
        attendances = current_app.db.execute_query("SELECT * FROM asistencias")
        return jsonify(attendances), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@attendance_routes_bp.route("/", methods=["POST"])
def register_attendance():
    """Registrar una nueva asistencia."""
    data = request.json
    query = """
    INSERT INTO asistencias (socio_id, fecha, tipo_ingreso)
    VALUES (%s, %s, %s)
    """
    params = (data["socio_id"], data["fecha"], data.get("tipo_ingreso", "normal"))
    try:
        current_app.db.execute_update(query, params)
        return jsonify({"message": "Asistencia registrada exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
