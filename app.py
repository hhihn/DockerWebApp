from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

# Startzeit merken
START_TIME = datetime.datetime.now()


@app.route('/')
def home():
    return '<h1>Meine Flask App</h1>'


@app.route('/health')
def health():
    """Einfacher Health Check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200


@app.route('/health/detailed')
def health_detailed():
    """Detaillierter Health Check"""
    uptime = datetime.datetime.now() - START_TIME

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'uptime_seconds': int(uptime.total_seconds()),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'checks': {
            'app': 'running',
            'memory': 'ok'
        }
    }), 200


@app.route('/health/live')
def liveness():
    """Liveness Probe - Läuft die App noch?"""
    return jsonify({'status': 'alive'}), 200


@app.route('/health/ready')
def readiness():
    """Readiness Probe - Ist die App bereit für Traffic?"""
    ready = True

    if ready:
        return jsonify({'status': 'ready'}), 200
    else:
        return jsonify({'status': 'not ready'}), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)