from flask import Flask, render_template, jsonify, request
import mysql.connector

from routes.risk import risk_bp
from routes.live import live_bp

app = Flask(__name__)

app.register_blueprint(risk_bp)
app.register_blueprint(live_bp)


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="rua"
    )


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# =========================
# STATUS API
# =========================

@app.route("/api/status")
def status():

    conn = get_db()
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

    if not row:
        return jsonify({})

    return jsonify({
        "device_id": row["device_id"],
        "presence": row["presence_status"],
        "touch": row["touch_activity"],
        "risk_score": row["risk_score"],
        "risk_level": row["risk_level"]
    })


# =========================
# GET TELEMETRY
# =========================

@app.route("/api/telemetry", methods=["GET"])
def telemetry():

    conn = get_db()
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

    return jsonify(row if row else {})


# =========================
# POST TELEMETRY
# =========================

@app.route("/api/telemetry", methods=["POST"])
def receive_telemetry():

    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO telemetry_logs
        (
            device_id,
            presence_status,
            touch_activity,
            movement_score,
            temperature,
            humidity,
            risk_score,
            risk_level
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        data["device_id"],
        data["presence_status"],
        data["touch_activity"],
        data["movement_score"],
        data["temperature"],
        data["humidity"],
        data["risk_score"],
        data["risk_level"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "saved"
    })


# =========================
# EVENTS API
# =========================

@app.route("/api/events")
def events():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM security_events
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(debug=True)