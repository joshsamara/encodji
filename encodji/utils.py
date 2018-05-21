"""
Utility functions.
"""

import os
import json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
EMOJI_FILE = os.path.join(CURRENT_DIR, '..', 'lib', 'emojis.json')

def load_emojis(file=EMOJI_FILE):
    with open(EMOJI_FILE, 'r') as emoji_data:
        return json.load(emoji_data)['emojis']
