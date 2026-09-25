import random

from database.db import get_connection
from services.risk_engine import calculate_risk

conn = get_connection()

for i in range(20):

    presence = random.random()
    touch = random.random()
    movement = random.random()
    environment = random.random()

    risk_score, risk_level = calculate_risk(
        presence,
        touch,
        movement,
        environment
    )

    conn.execute("""
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
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
    """,
    (
        "Endpoint01",
        "Present",
        1,
        movement,
        28,
        65,
        risk_score,
        risk_level
    ))

conn.commit()
conn.close()

print("Demo data generated")