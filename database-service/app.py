from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# In-Memory Datenbank
DATA = {}


@app.route('/db/get/<key>')
def get_value(key):
    if key in DATA:
        return jsonify({
            'key': key,
            'value': DATA[key],
            'found': True
        })
    return jsonify({
        'key': key,
        'error': 'Key not found',
        'found': False
    }), 404


@app.route('/db/set/<key>', methods=['POST'])
def set_value(key):
    data = request.get_json()

    if not data or 'value' not in data:
        return jsonify({'error': 'Missing value'}), 400

    DATA[key] = data['value']

    return jsonify({
        'key': key,
        'value': DATA[key],
        'message': 'Stored successfully'
    }), 201


@app.route('/db/all')
def get_all():
    return jsonify({
        'data': DATA,
        'count': len(DATA),
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/health')
def health():
    return jsonify({
        'service': 'database-service',
        'status': 'healthy',
        'entries': len(DATA),
        'timestamp': datetime.datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)