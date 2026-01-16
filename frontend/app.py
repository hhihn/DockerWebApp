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
    try:
        response = requests.get(f'{API_URL}/api/users', timeout=5)
        users = response.json()
        return f'''
            <h1>Benutzer vom API Service</h1>
            <pre>{users}</pre>
            <a href="/">Zurück</a>
        '''
    except Exception as e:
        return f'<h1>Fehler</h1><p>{str(e)}</p>', 500

@app.route('/health')
def health():
    # Prüfe ob API erreichbar
    try:
        response = requests.get(f'{API_URL}/health', timeout=2)
        api_status = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        api_status = 'unreachable'

    return jsonify({
        'service': 'frontend',
        'status': 'healthy',
        'dependencies': {
            'api-service': api_status
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)