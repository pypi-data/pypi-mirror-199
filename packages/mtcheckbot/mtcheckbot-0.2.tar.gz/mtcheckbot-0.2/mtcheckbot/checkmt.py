import requests
import json

class checkmt5:
    def getMtg():

        url = 'https://salardev.com/apps/checkmt5.json'
        response = requests.get(url)

        if response.ok:
            data = json.loads(response.content)
            return data['mt5']['allowed']
        