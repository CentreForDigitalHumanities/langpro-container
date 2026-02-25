import pytest

from server import app


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
