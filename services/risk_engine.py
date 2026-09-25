from services.alert_manager import create_event

def calculate_risk(
    presence,
    touch,
    movement,
    environment
):

    score = (
        (presence * 0.25)
        + (touch * 0.25)
        + (movement * 0.35)
        + (environment * 0.15)
    ) * 100

    if score <= 30:

        level = "Low"

    elif score <= 60:

        level = "Medium"

        create_event(
            "Behavior",
            "Warning",
            "Behavioral anomaly detected"
        )

    else:

        level = "High"

        create_event(
            "Security",
            "Critical",
            "Critical risk detected"
        )

    return round(score,2), level