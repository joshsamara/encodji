"""
Encoders and decoding utilities.
"""

EMOJIS = [
    '\U0001F947',
    '\U0001F948',
    '\U0001F949'
]
SPACE = len(EMOJIS)


def _special_format(code):
    emojis = []
    while code > 0:
        emojis.append(EMOJIS[code % SPACE])
        code //= SPACE
    return "!{}!".format(''.join(emojis))


def encode_char(char):
    code = ord(char)
    if code < SPACE:
        # If we fit in the space, just return that emoji
        return EMOJIS[code]
    # Otherwise return a set of emojis
    return _special_format(code)


def encode_string(string):
    return ''.join(encode_char(c) for c in string)


def decode_char(char):
    pass


def decode_string(string):
    pass


print(encode_string('abc'))
