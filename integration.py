import requests


def sendDiscord(mensagem, channelId, token):
    result = requests.post(f'https://discord.com/api/webhooks/{channelId}/{token}', data={'content': mensagem})
    return result.status_code == 200
