"""
Fetches and saves emojis to disk.
"""

import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

EMOJI_INDEX = 'https://unicode.org/emoji/charts/full-emoji-list.html'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
EMOJI_FILE = os.path.join(CURRENT_DIR, '..', 'lib', 'emojis.json')

def _get_all_codes():
    data = requests.get(EMOJI_INDEX).text
    parsed = bs(data, 'html.parser')
    return (td.text for td in parsed.find_all('td', class_='code'))

def _code_to_emoji(code):
    tmp = (int(c.lstrip('U+'), 16) for c in code.split(' '))
    return ''.join(chr(t) for t in tmp)

def _write_to_file(emojis):
    with open(EMOJI_FILE, 'r') as emoji_data:
        data = json.load(emoji_data)

    existing_emojis = data['emojis']
    # Only write a file if we have more emojis to write
    if len(existing_emojis) < len(emojis):
        with open(EMOJI_FILE, 'w') as emoji_data:
            data = {
                'emojis': emojis,
                '_meta': {
                    'date': datetime.now().isoformat()
                }
            }
            json.dump(data, emoji_data)
        return True
    else:
        return False


if __name__ == '__main__':
    print("Fetching emojis")
    codes  = _get_all_codes()
    emojis = list(_code_to_emoji(code) for code in codes)
    _write_to_file(emojis)
