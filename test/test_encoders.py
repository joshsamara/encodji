"""Encoder tests."""

from hypothesis import given
from hypothesis.strategies import text

from encodji.encoders import encode, decode

@given(text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s
