import pytest
import json
from pathlib import Path
from server import app

DATA_DIR = Path(__file__).parent / "tests" / "data"

# read all sentence and prolog ccg derivation pairs
with open(DATA_DIR / "ccg_pl.json", encoding="utf-8") as F:
    SEN_TO_CCGPL = json.load(F)



@pytest.fixture
def testapp():
    app.config.update({
        'TESTING': True
    })
    yield app


@pytest.fixture
def client(testapp):
    return testapp.test_client()


def test_parse_and_prove(client):
    payload = {
        'prover_config': ['allInt', 'aall'],
        'premises': [
            'A group of kids is playing in a yard and an old man is standing in the background'
        ],
        'knowledge_bases': [],
        'hypothesis': 'A group of boys in a yard is playing and a man is standing in the background',
        'ral': 200,
        'senses': 'all',
        'format': 'annotator'
    }
    response = client.post('/prove/', json=payload)
    assert response.status_code == 200



# testing api call with already parsed sentences
@pytest.mark.parametrize("premises, hypothesis",
    [
        (premises, hypothesis)
        for premises, hypothesis in [
            (["John runs"], "John moves")
        ]
    ])
def test_parse_and_prove_WITH_already_parsed_input(client, premises, hypothesis):
    payload = {
        'prover_config': ['allInt'],
        'premises': premises,
        'knowledge_bases': [],
        'hypothesis': hypothesis,
        'parsed': {'premises': [SEN_TO_CCGPL[p] for p in premises],
                   'hypothesis': SEN_TO_CCGPL[hypothesis]
                },
        'parser': 'WHATEVER',
        'ral': 200,
        'senses': 'all',
        'format': 'annotator'
    }
    response = client.post('/prove/', json=payload)
    assert response.status_code == 200