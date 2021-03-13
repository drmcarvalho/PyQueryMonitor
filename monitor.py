from database import _query


def sqlmonitor(connection, time='30'):
    yield from _query(
        connection,
        """
        SELECT 
            ID, USER, HOST, DB, TIME, STATE, INFO
        FROM
            INFORMATION_SCHEMA.PROCESSLIST
        WHERE   
            command <> 'Sleep' AND time >= %s;""",
        params=[time],
    )
