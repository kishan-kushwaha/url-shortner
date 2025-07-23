from flask import Flask, jsonify, request, redirect, abort
from .utils import generate_short_code, is_valid_url, build_short_url
from .models import save_mapping, get_mapping, increment_clicks

app = Flask(__name__)


@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })


@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate a unique code
    code = generate_short_code()
    while get_mapping(code) is not None:
        code = generate_short_code()

    save_mapping(code, original_url)
    short_url = build_short_url(code)
    return jsonify({
        "short_code": code,
        "short_url": short_url
    })


@app.route('/<code>')
def redirect_short_url(code):
    entry = get_mapping(code)
    if entry is None:
        abort(404)
    increment_clicks(code)
    return redirect(entry.original_url)


@app.route('/api/stats/<code>')
def url_stats(code):
    entry = get_mapping(code)
    if entry is None:
        return jsonify({"error": "Code not found"}), 404
    return jsonify({
        "url": entry.original_url,
        "clicks": entry.click_count,
        "created_at": entry.created_at.isoformat() + "Z"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)