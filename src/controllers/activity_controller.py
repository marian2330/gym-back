from flask import Blueprint, request, jsonify, current_app

activity_routes_bp = Blueprint("activity_routes", __name__, url_prefix="/actividades")

# Obtener todas las actividades
@activity_routes_bp.route("/", methods=["GET"])
def get_activities():
    """Obtener la lista de todas las actividades."""
    try:
        activities = current_app.db.execute_query("SELECT * FROM actividades")
        return jsonify(activities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Agregar una nueva actividad
@activity_routes_bp.route("/", methods=["POST"])
def add_activity():
    """Agregar una nueva actividad."""
    data = request.json
    query = """
    INSERT INTO actividades (nombre, dias_habilitados, horario, precio)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        data["nombre"],
        data.get("dias_habilitados"),
        data.get("horario"),
        data.get("precio")
    )
    try:
        current_app.db.execute_update(query, params)
        return jsonify({"message": "Actividad agregada exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una actividad por su ID
@activity_routes_bp.route("/<int:activity_id>", methods=["GET"])
def get_activity(activity_id):
    """Obtener los detalles de una actividad específica."""
    try:
        query = "SELECT * FROM actividades WHERE id = %s"
        activity = current_app.db.execute_query(query, (activity_id,))
        if not activity:
            return jsonify({"message": "Actividad no encontrada."}), 404
        return jsonify(activity[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar una actividad existente
@activity_routes_bp.route("/<int:activity_id>", methods=["PUT"])
def update_activity(activity_id):
    """Actualizar los detalles de una actividad."""
    data = request.json
    query = """
    UPDATE actividades
    SET nombre = %s, dias_habilitados = %s, horario = %s, precio = %s
    WHERE id = %s
    """
    params = (
        data["nombre"],
        data.get("dias_habilitados"),
        data.get("horario"),
        data.get("precio"),
        activity_id
    )
    try:
        rows_affected = current_app.db.execute_update(query, params)
        if rows_affected == 0:
            return jsonify({"message": "Actividad no encontrada o no se realizaron cambios."}), 404
        return jsonify({"message": "Actividad actualizada exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una actividad
@activity_routes_bp.route("/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    """Eliminar una actividad."""
    try:
        query = "DELETE FROM actividades WHERE id = %s"
        rows_affected = current_app.db.execute_update(query, (activity_id,))
        if rows_affected == 0:
            return jsonify({"message": "Actividad no encontrada."}), 404
        return jsonify({"message": "Actividad eliminada exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
