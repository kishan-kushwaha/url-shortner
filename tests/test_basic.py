import pytest
from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_shorten_and_redirect_and_stats(client):
    original = "https://www.example.com/test"
    resp = client.post('/api/shorten', json={"url": original})
    assert resp.status_code == 200
    data = resp.get_json()
    code = data['short_code']
    assert len(code) == 6
    assert "short_url" in data

    redirect_resp = client.get(f'/{code}', follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers['Location'] == original

    stats_resp = client.get(f'/api/stats/{code}')
    assert stats_resp.status_code == 200
    stats = stats_resp.get_json()
    assert stats['url'] == original
    assert stats['clicks'] == 1
    assert 'created_at' in stats


def test_shorten_invalid_url(client):
    resp = client.post('/api/shorten', json={"url": "not_a_url"})
    assert resp.status_code == 400


def test_stats_not_found(client):
    resp = client.get('/api/stats/unknown')
    assert resp.status_code == 404