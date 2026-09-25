from database.db import get_connection

def create_event(
    event_type,
    severity,
    description
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO security_events
        (
            event_type,
            severity,
            description
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
    """,
    (
        event_type,
        severity,
        description
    ))

    conn.commit()
    conn.close()