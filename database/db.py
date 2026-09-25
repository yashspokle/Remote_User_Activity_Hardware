import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="rua"
    )

def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS telemetry_logs(
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        device_id VARCHAR(50),
        presence_status VARCHAR(20),
        touch_activity INT,
        movement_score FLOAT,
        temperature FLOAT,
        humidity FLOAT,
        risk_score FLOAT,
        risk_level VARCHAR(20)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS security_events(
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        event_type VARCHAR(100),
        severity VARCHAR(20),
        description TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()