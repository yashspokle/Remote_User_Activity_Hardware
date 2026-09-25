import json
import paho.mqtt.publish as publish

publish.single(
    "telemetry/movement",
    json.dumps({
        "value": 8
    }),
    hostname="localhost"
)

print("Message Sent")