from flask import Blueprint, request, jsonify, current_app

employee_routes_bp = Blueprint("employee_routes", __name__, url_prefix="/empleados")

@employee_routes_bp.route("/", methods=["GET"])
def get_employees():
    """Obtener la lista de empleados."""
    try:
        employees = current_app.db.execute_query("SELECT * FROM empleados")
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_routes_bp.route("/", methods=["POST"])
def add_employee():
    """Agregar un nuevo empleado."""
    data = request.json
    query = """
    INSERT INTO empleados (nombre, apellido, email, telefono, direccion, puesto, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data["nombre"], data["apellido"], data["email"],
        data.get("telefono"), data.get("direccion"), data["puesto"], data["password"]
    )
    try:
        current_app.db.execute_update(query, params)
        return jsonify({"message": "Empleado agregado exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
