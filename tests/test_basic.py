import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    resp = client.get('/')
    assert resp.status_code == 200
    j = resp.get_json()
    assert j['status'] == 'healthy'
    assert j['service'] == 'URL Shortener API'


def test_api_health(client):
    resp = client.get('/api/health')
    assert resp.status_code == 200
    j = resp.get_json()
    assert j['status'] == 'ok'


def test_shorten_redirect_stats(client):
    original = 'https://example.com'
    resp = client.post('/api/shorten', json={'url': original})
    assert resp.status_code == 200
    data = resp.get_json()
    code = data['short_code']
    assert len(code) == 6
    assert 'short_url' in data

    redir = client.get(f'/{code}', follow_redirects=False)
    assert redir.status_code == 302
    assert redir.headers['Location'] == original

    stats = client.get(f'/api/stats/{code}').get_json()
    assert stats['url'] == original
    assert stats['clicks'] == 1
    assert 'created_at' in stats


def test_invalid_url(client):
    resp = client.post('/api/shorten', json={'url': 'foo'})
    assert resp.status_code == 400


def test_stats_not_found(client):
    resp = client.get('/api/stats/unknown')
    assert resp.status_code == 404