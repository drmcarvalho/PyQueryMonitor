from pymysql import connect, cursors


def database(user, password, host, port):
    return connect(user=user,
                   passwd=password,
                   host=host,
                   port=port,
                   cursorclass=cursors.DictCursor)


def _query(connection, statement, params=None):
    with connection.cursor() as cur:
        if params:
            cur.execute(statement, params)
        else:
            cur.execute(statement)
        for row in cur:
            yield row
