from database.db import get_connection
import random

conn = get_connection()

for i in range(20):

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
        (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "Endpoint01",
        "Present",
        1,
        random.randint(0,10),
        random.randint(25,35),
        random.randint(50,70),
        random.randint(10,90),
        "Low"
    ))

conn.commit()
conn.close()

print("Data inserted")