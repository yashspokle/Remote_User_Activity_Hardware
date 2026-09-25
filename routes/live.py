from flask import Blueprint, jsonify
from database.db import get_connection

live_bp = Blueprint(
    "live",
    __name__
)

@live_bp.route("/api/live")
def live():
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM telemetry_logs
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return jsonify(dict(row))

    return jsonify({})