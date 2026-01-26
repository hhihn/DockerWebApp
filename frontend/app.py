from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# lese die umgebungsvariable aus dem container aus und speichere sie in die
# variable
DB_URL = os.getenv('DB_URL')

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
        # hole die daten aus dem database service
        # und wandle sie in ein dictionary um
        response = requests.get(DB_URL + "/db/all", timeout=5).json()

        html = '<h1>Benutzer</h1><table border="1">'
        html += '<tr><th>ID</th><th>Name</th><th>Email</th></tr>'

        users = response.get('data', {})

        # iteriere über das dictionary
        for key, user in users.items():
            html += f"<tr><td>{user.get('id', 'N/A')}</td><td>{user.get('name', 'N/A')}</td><td>{user.get('email', 'N/A')}</td></tr>"

        html += '</table>'
        html += f"<p>Anzahl: {response.get('count', 0)}</p>"
        html += '<a href="/">Zurück</a>'
        return html, 200
    except Exception as e:
        return f'<h1>Fehler: {str(e)}</h1><p></p>', 500

@app.route('/health')
def health():

    return jsonify({
        'service': 'frontend',
        'status': 'healthy',
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)