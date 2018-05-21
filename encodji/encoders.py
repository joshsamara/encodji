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


def _find_next(string, start, c):
    """Find the next occurance of c in the string AFTER the start index.

    Returns:
        Tuple of (int, string) where the int is the index of c and the
        string is the string of characters found while iterating.
    Notes:
        Used while parsing so we don't have to create substrings and use .index
    """
    i = start + 1
    collected = []
    while string[i] != c:
        collected.append(string[i])
        i += 1
    return (i, ''.join(collected))


def _encode_simple(code):
    """Get an emoji based on a given code (return value from ord)>

    Notes:
        - Assumes the code is less than SPACE
        - If the emoji is a multi-character emoji, surrounds in a surround char.
    """
    emoji = EMOJIS[code]
    if len(emoji) > 1:
        return f'{MULTI_INDICATOR}{emoji}{MULTI_INDICATOR}'
    return emoji


def _decode_simple(emoji):
    """Decode a simple emoji to a single character."""
    return chr(EMOJIS.index(emoji))


def _encode_special(code):
    """Create a string of special-encoded emojis.

    Uses the list of emojis as a Numeral system where the value of the emoji
    is equal to its index in the list and a base of the lenght of the list

    Notes:
        - This is necessary for characters with an ord greater than the number
        of emojis.
        - Special-encoded emojis are surrounded by a special indicator.
    """
    emojis = []
    while code > 0:
        encode_index = code % SPACE
        emojis.append(_encode_simple(encode_index))
        code //= SPACE
    str_emojis = ''.join(emojis)
    return f'{SPECIAL_INDICATOR}{str_emojis}{SPECIAL_INDICATOR}'


def _decode_special(chars):
    """Decodes a string of special emojis into a character."""
    exp = total = idx = 0
    while idx < len(chars):
        char = chars[idx]
        if char == MULTI_INDICATOR:
            # Special encoded emojis may also contain multi-emojis
            matching_idx, multi_chars = _find_next(chars, idx, MULTI_INDICATOR)
            idx = matching_idx + 1  # Jump until after the multi-emoji
            emoji = ''.join(multi_chars)
        else:
            # If not a multi-emoji then the char is just a single emoji
            emoji = char
            idx += 1
        total += EMOJIS.index(emoji) * SPACE ** exp
        exp += 1
    return chr(total)


def _encode_char(char):
    """Encode a single character into an emoji.

    Chooses between doing a simple or special encoding.

    Note:
        There's no equivalent 'decode_char' because we can't simply decode
        one character at a time due to multi-emojis and special encoding.
    """
    code = ord(char)
    if code < SPACE:
        # If we fit in the space, just return that emoji
        return _encode_simple(code)
    # Otherwise return a set of emojis
    return _encode_special(code)


def generate_encoded(iterable):
    """Generate encoded characters from an iterable of chars."""
    return (_encode_char(c) for c in iterable)


def generate_decoded(encoded):
    """Generate decoded characters from a string of encoded chars.

    TODO: Make this work with an iterable (we'll need it for file reading)
    """
    idx = 0
    while idx < len(encoded):
        char = encoded[idx]
        if char == SPECIAL_INDICATOR:
            # Grab a set of emojis up to the next '!' to decode
            matching_idx, chars = _find_next(encoded, idx, SPECIAL_INDICATOR)
            idx = matching_idx + 1
            yield _decode_special(chars)
        elif char == MULTI_INDICATOR:
            # We have a multi-character emoji
            matching_idx, chars = _find_next(encoded, idx, MULTI_INDICATOR)
            idx = matching_idx + 1
            yield _decode_simple(chars)
        else:
            # If we have a simple encoding, simple decode it
            idx += 1
            yield _decode_simple(char)


def encode_string(string):
    """Create an enocoded string of text."""
    return ''.join(generate_encoded(string))


def decode_string(encoded):
    """Create a decoded string of text."""
    return ''.join(generate_decoded(encoded))


# Super simple sanity checks
original = 'Thîs is Tôtally a TéS†®.'
encoded = encode_string(original)
decoded = decode_string(encoded)
print(f"""
Test single encode:

Original: {original}
Encoded:  {encoded}
Decoded:  {decoded}
""")
assert original == decoded

# We should be able to doubly encoded/decode
double_encoded = encode_string(encoded)
single_decoded = decode_string(double_encoded)
double_decoded = decode_string(single_decoded)
print(f"""
Test Double encode:

Original:       {original}
Single encoded: {encoded}
Double encoded: {double_encoded}
Single decoded: {single_decoded}
Double decoded: {double_decoded}
""")
assert double_decoded == original
