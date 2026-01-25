from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_URL = os.getenv('API_URL', 'http://api-service:5001')

@app.route('/')
def home():
    return '''
        <h1>Frontend Service</h1>
        <p><a href="/users">Benutzer laden</a></p>
        <p><a href="/health">Health Check</a></p>
    '''

@app.route('/users')
def get_users():
    return '<h1>Fehler</h1><p></p>', 500

@app.route('/health')
def health():

    return jsonify({
        'service': 'frontend',
        'status': 'healthy',
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)