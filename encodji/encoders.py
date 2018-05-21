"""
Encoders and decoding utilities.
"""

EMOJIS = [
    '\U0001F947',
    '\U0001F948',
    '\U0001F949'
]
SPACE = len(EMOJIS)
SPECIAL_INDICATOR = '!'


def _encode_special(code):
    emojis = []
    while code > 0:
        emojis.append(EMOJIS[code % SPACE])
        code //= SPACE
    return "{indicator}{emojis}{indicator}".format(
        indicator=SPECIAL_INDICATOR,
        emojis=''.join(emojis)
    )


def _decode_special(emojis):
    exp = 0
    total = 0
    for emoji in emojis:
        total += EMOJIS.index(emoji) * SPACE ** exp
        exp += 1
    return chr(total)


def _encode_char(char):
    code = ord(char)
    if code < SPACE:
        # If we fit in the space, just return that emoji
        return EMOJIS[code]
    # Otherwise return a set of emojis
    return _encode_special(code)


def generate_encoded(string):
    return (_encode_char(c) for c in string)


def encode_string(string):
    return ''.join(generate_encoded(string))


def _decode_simple(emoji):
    return chr(EMOJIS.index(emoji))


def _find_next(string, start, c):
    """Find the next occurance of c in the string AFTER the start index.

    Returns:
        Tuple of (int, string) where the int is the index of c and the
        string is the string of characters found while iterating.
    """
    i = start + 1
    collected = []
    while string[i] != c:
        collected.append(string[i])
        i += 1
    return (i, ''.join(collected))


def generate_decoded(encoded):
    i = 0
    # TODO: we need a thing for multi-character emojis
    while i < len(encoded):
        c = encoded[i]
        if c != '!':
            # If we have a regular characet
            yield _decode_simple(c)
            i += 1
        else:
            # Grab a set of emojis up to the next '!' to decode
            matching_idx, emojis = _find_next(encoded, i, '!')
            yield _decode_special(emojis)
            i = matching_idx + 1


def decode_string(encoded):
    return ''.join(generate_decoded(encoded))

original = 'Thîs is Tôtally a TéS†®.'
encoded = encode_string(original)
print(encoded)
decoded = decode_string(encoded)
assert original == decoded
