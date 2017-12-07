import falcon
from falcon import testing
import msgpack
import pytest

from myFalconApp.app import api

@pytest.fixture
def client():
	return testing.TestClient(api)


def test_list_carts(client):
	doc = {
		'carts': ['hello']
	}

	response = client.simulate_get('/carts')
	result_doc = msgpack.unpackb(response.content, encoding='utf-8')

	assert result_doc == doc
	assert response.status == falcon.HTTP_OK


