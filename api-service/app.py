from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# Simulierte Datenbank
USERS = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
]

@app.route('/api/users')
def get_users():
    return jsonify({
        'users': USERS,
        'count': len(USERS),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/health')
def health():
    return jsonify({
        'service': 'api-service',
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)