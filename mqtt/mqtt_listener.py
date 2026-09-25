import json
import paho.mqtt.client as mqtt

from database.db import get_connection


BROKER = "localhost"
PORT = 1883

TOPICS = [
    ("telemetry/presence", 0),
    ("telemetry/touch", 0),
    ("telemetry/movement", 0),
    ("telemetry/environment", 0)
]


latest_data = {
    "presence": 0,
    "touch": 0,
    "movement": 0,
    "temperature": 0,
    "humidity": 0
}


def save_to_db():

    conn = get_connection()

    risk_score = (
        latest_data["movement"] * 5
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
            ?,?,?,?,?,?,?,?
        )
    """,
    (
        "Endpoint01",
        str(latest_data["presence"]),
        latest_data["touch"],
        latest_data["movement"],
        latest_data["temperature"],
        latest_data["humidity"],
        risk_score,
        "Low"
    ))

    conn.commit()
    conn.close()


def on_connect(
    client,
    userdata,
    flags,
    rc,
    properties=None
):

    print("Connected")

    client.subscribe(TOPICS)


def on_message(
    client,
    userdata,
    msg
):

    payload = json.loads(
        msg.payload.decode()
    )

    topic = msg.topic

    if topic == "telemetry/presence":

        latest_data["presence"] = payload["value"]

    elif topic == "telemetry/touch":

        latest_data["touch"] = payload["value"]

    elif topic == "telemetry/movement":

        latest_data["movement"] = payload["value"]

    elif topic == "telemetry/environment":

        latest_data["temperature"] = payload["temperature"]

        latest_data["humidity"] = payload["humidity"]

    save_to_db()

    print(
        "Saved telemetry"
    )


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect

client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

client.loop_forever()