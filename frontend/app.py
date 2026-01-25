from flask import Flask
import requests
import os

app = Flask(__name__)

DB_URL = os.getenv('DB_URL', 'http://database-service:5002')


@app.route('/')
def home():
    return '''
        <h1>User-Verwaltung</h1>
        <ul>
            <li><a href="/users">Alle User anzeigen</a></li>
            <li><a href="/health">System-Status</a></li>
        </ul>
    '''


@app.route('/users')
def show_users():
    """User über API-Service laden"""
    try:
        response = requests.get(f'{DB_URL}/db/all', timeout=5)
        data = response.json()

        html = '<h1>Benutzerasdfasdfsadf</h1><table border="1">'
        html += '<tr><th>ID</th><th>Name</th><th>Email</th></tr>'

        # data['data'] ist ein Dict, nicht eine Liste!
        users = data.get('data', {})

        for key, user in users.items():  # ← .items() für Dict
            html += f"<tr><td>{user['id']}</td><td>{user['name']}</td><td>{user['email']}</td></tr>"

        html += '</table>'
        html += f"<p>Anzahl: {data.get('count', 0)}</p>"
        html += '<a href="/">Zurück</a>'

        return html

    except Exception as e:
        return f'<h1>Fehler</h1><p>{e}</p>', 500

@app.route('/health')
def health():
    """Prüfe alle Services"""

    # API-Service prüfen (der prüft Database-Service)
    try:
        response = requests.get(f'{DB_URL}/health', timeout=2)
        api_health = response.json()
    except:
        api_health = {'status': 'unreachable'}

    return f'''
        <h1>System-Status</h1>
        <table border="1">
            <tr><th>Service</th><th>Status</th></tr>
            <tr><td>Frontend</td><td>healthy</td></tr>
            <tr><td>Database-Service</td><td>{api_health.get('dependencies', {}).get('database-service', 'unknown')}</td></tr>
        </table>
        <a href="/">Zurück</a>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)