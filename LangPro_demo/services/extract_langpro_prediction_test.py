import pytest
from .extract_langpro_prediction import extract_langpro_prediction

_CLOSED = ["al", "closed", "Ter", 8]
_OPEN = ["na", "open", "Ter", 16]
_FAILED = ["na", "Ter", 16]
_EMPTY = []

# (entailment_info, contradiction_info, expected)
# None means the key is absent from the proofs dict entirely.
CASES = [
    (_CLOSED, _OPEN, "entailment"),
    (_CLOSED, _FAILED, "entailment"),
    (_CLOSED, None, "entailment"),

    (_OPEN, _CLOSED, "contradiction"),
    (_FAILED, _CLOSED, "contradiction"),
    (None, _CLOSED, "contradiction"),

    (_FAILED, _FAILED, "unknown"),
    (None, None, "unknown"),
    (_EMPTY, _EMPTY, "unknown"),

    (_OPEN, _OPEN, "neutral"),
    (_OPEN, _FAILED, "neutral"),
    (_FAILED, _OPEN, "neutral"),

    (_CLOSED, _CLOSED, "conflict"),
    (_FAILED, _FAILED, "unknown"),
]


def make_proofs(entailment_info, contradiction_info):
    proofs = {}
    for key, info in [
        ("entailment", entailment_info),
        ("contradiction", contradiction_info),
    ]:
        if info is None:
            continue
        else:
            proofs[key] = {"info": info, "proof": {}}
    return proofs


@pytest.mark.parametrize("entailment_info,contradiction_info,expected", CASES)
def test_extract_langpro_prediction(entailment_info, contradiction_info, expected):
    proofs = make_proofs(entailment_info, contradiction_info)
    assert extract_langpro_prediction(proofs) == expected
