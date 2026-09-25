from flask import Blueprint,jsonify
from database.db import get_connection

risk_bp = Blueprint(
    "risk",
    __name__
)

@risk_bp.route("/api/risk-history")
def risk_history():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT timestamp,risk_score
    FROM telemetry_logs
    ORDER BY id DESC
    LIMIT 50
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(
        [dict(row) for row in rows]
    )