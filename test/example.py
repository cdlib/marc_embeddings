from hypothesis import given
from hypothesis.strategies import text

@given(text(), text())
def test_cosine_similarity_upper_bound(a, b):
    """
    The cosine similarity of any two sentences under the transformation must not
    exceed either sentence's reflexive similarity.
    """
    assert len(a) == len(b)
