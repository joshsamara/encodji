"""
Encoders and decoding utilities.
"""

EMOJIS = [
    '\U0001F947',
    '\U0001F948',
    '\U0001F949',
    # Test for multi-character emojis
    '\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F'
]
SPACE = len(EMOJIS)
SPECIAL_INDICATOR = '!'
MULTI_INDICATOR = ' '


def _encode_simple(index):
    emoji = EMOJIS[index]
    if len(emoji) > 1:
        return '{indicator}{emoji}{indicator}'.format(
            indicator=MULTI_INDICATOR,
            emoji=emoji
        )
    return emoji


def _encode_special(code):
    emojis = []
    while code > 0:
        encode_index = code % SPACE
        emojis.append(_encode_simple(encode_index))
        code //= SPACE
    return "{indicator}{emojis}{indicator}".format(
        indicator=SPECIAL_INDICATOR,
        emojis=''.join(emojis)
    )


def _decode_special(chars):
    exp = 0
    total = 0
    i = 0
    while i < len(chars):
        emoji_ref = chars[i]
        if emoji_ref == MULTI_INDICATOR:
            # Special encoded emojis may also contain multi-emojis
            matching_idx, multi_chars = _find_next(chars, i, MULTI_INDICATOR)
            i = matching_idx + 1
            emoji = ''.join(multi_chars)
        else:
            emoji = emoji_ref
            i += 1
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
        if c == SPECIAL_INDICATOR:
            # Grab a set of emojis up to the next '!' to decode
            matching_idx, chars = _find_next(encoded, i, SPECIAL_INDICATOR)
            i = matching_idx + 1
            yield _decode_special(chars)
        elif c == MULTI_INDICATOR:
            # We have a multi-character emoji
            matching_idx, chars = _find_next(encoded, i, MULTI_INDICATOR)
            i = matching_idx + 1
            yield _decode_simple(chars)
        else:
            # If we have a simple encoding, simple decode it
            i += 1
            yield _decode_simple(c)


def decode_string(encoded):
    return ''.join(generate_decoded(encoded))


original = 'Thîs is Tôtally a TéS†®.'
encoded = encode_string(original)
decoded = decode_string(encoded)
assert original == decoded
