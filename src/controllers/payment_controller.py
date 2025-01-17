from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

payment_routes_bp = Blueprint("payment_routes", __name__, url_prefix="/cuotas")

@payment_routes_bp.route("/", methods=["GET"])
def get_cuotas():
    """Obtener la lista de todas las cuotas."""
    try:
        cuotas = current_app.db.execute_query("SELECT * FROM cuotas")
        return jsonify(cuotas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_routes_bp.route("/", methods=["POST"])
def create_payment():
    """Registrar un pago y activar la membresía del socio."""
    try:
        data = request.get_json()
        socio_id = data.get("socio_id")
        monto = data.get("monto")

        if not socio_id or not monto:
            return jsonify({"error": "Faltan datos requeridos (socio_id, monto)."}), 400

        # Verificar si el socio existe
        socio = current_app.db.execute_query(
            "SELECT * FROM socios WHERE id = %s", (socio_id,)
        )
        if not socio:
            return jsonify({"error": "El socio no existe."}), 404

        # Calcular fechas
        fecha_pago = datetime.utcnow()
        fecha_inicio = fecha_pago
        fecha_fin = fecha_inicio + timedelta(days=30)

        # Registrar el pago
        current_app.db.execute_query(
            """
            INSERT INTO cuotas (socio_id, fecha_pago, fecha_inicio, fecha_fin, estado, monto)
            VALUES (%s, %s, %s, %s, 'activa', %s)
            """,
            (socio_id, fecha_pago, fecha_inicio, fecha_fin, monto),
        )

        # Actualizar estado del socio a "activo"# Actualizar estado del socio a "activo"
        current_app.db.execute_update(
            "UPDATE socios SET estado = 'activo' WHERE id = %s",  # Consulta
            (socio_id,)  # Parámetros en tupla
        )

        # Actualizar estado de las cuotas a "activa" para el socio especificado
        current_app.db.execute_update(
            "UPDATE cuotas SET estado = 'activa' WHERE socio_id = %s",  # Consulta
            (socio_id,)  # Parámetros en tupla
        )

            
        return jsonify({
            "message": "Pago registrado y membresía activada.",
            "payment": {
                
                "socio_id": socio_id,
                "fecha_pago": fecha_pago.strftime("%Y-%m-%d"),
                "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                "monto": monto,
                
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
