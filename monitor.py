from database import _query
import requests


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


def sendDiscord(mensagem, channelId, token):
    result = requests.post(f'https://discord.com/api/webhooks/{channelId}/{token}', data={'content': mensagem})
    return result.status_code == 200
