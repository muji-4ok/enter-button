import requests
import utils
import random
from pathlib import Path
import re


line = random.choice(open("model/insults.txt").readlines())
file_name = re.sub(r'[^\w]', '', line.replace(" ", "_"))
file = Path(f'insults/{file_name}.mp3')
if not file.exists():
    url = 'https://support.readaloud.app/ttstool/createParts'
    headers = {
        'Host': 'support.readaloud.app',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://ttstool.com',
        'Connection': 'keep-alive',
        'Referer': 'https://ttstool.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers'
    }
    payload = [{
        "voiceId": "Microsoft US English (David)",
        "ssml": f"<speak version=\"1.0\" xml:lang=\"en-US\">{line}</speak>"
    }]

    r = requests.post(url=url, headers=headers, json=payload)

    url = 'https://support.readaloud.app/ttstool/getParts'
    headers = {
        'Host': 'support.readaloud.app',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': '',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://ttstool.com',
        'Connection': 'keep-alive',
        'Referer': 'https://ttstool.com/',
        'Sec-Fetch-Dest': 'audio',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers'
    }

    params = {
        'q': f'{r.json()[0]}',
    }

    response = requests.get(url=url, headers=headers, params=params)

    # ToDo use absolute paths

    with open(f'insults/{file_name}.mp3', 'wb') as f:
        f.write(response.content)

utils.play_sound(f'insults/{file_name}.mp3')
