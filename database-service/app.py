from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# simulierte in-memory datenbank
DATA = {}

@app.route('/db/delete/<key>', methods=['DELETE'])
def delete_value(key):
    # TODO: Implementiere das Löschen eines Eintrags
    # - Falls Key existiert: löschen und Erfolgsmeldung zurückgeben
    # - Falls Key nicht existiert: 404 zurückgeben
    if key in DATA:
        DATA.pop(key)
        return jsonify({'status': 'success', 'key': key}), 200
    else:
        return jsonify({'error': 'Missing value'}), 404

@app.route('/db/all')
def get_all():
    return jsonify({'data': DATA,
                   'count': len(DATA),
                    'timestamp': datetime.datetime.now().isoformat()}), 200

# GET: daten laden
# POST: daten schreiben
# <key> ist eine sog. Path Variable, die der angehängten Methode als Argument übergeben wird
@app.route('/db/set/<key>', methods=['POST'])
def set_value(key):
    received_data = request.get_json()

    # überprüfe ob daten richtig zur verfügung gestellt werden
    # und gebe fehler zurück falls nicht
    if not received_data or "value" not in received_data:
        return jsonify({'error': 'Missing value'}), 400

    # falls daten korrekt sind, füge sie in die db ein
    DATA[key] = received_data['value']

    # gebe meldung zurück
    return jsonify({
        'status': 'success',
        'key': key,
        'value': DATA[key],
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'Data stored successfully'
    }), 201

# expose einen endpoint der einen gegeben key aus der db ausliest
# und zurücksendet
@app.route('/db/get/<key>', methods=['GET'])
def get_value(key):
    if key in DATA:
        return jsonify({'key': key,
                        'value': DATA[key],
                        'timestamp': datetime.datetime.now().isoformat()})
    else:
        return jsonify({'error': 'Key not found',
                        'key': key}), 404

# health check point wird regelmäßig von kubernetes aufgerufen
# um zu überprüfen, ob der Pod noch arbeitet. falls dies
# fehlschlägt, wird der pod neu gestartet
# fehlschlagen = keine Antwort
@app.route('/health')
def health():
    return jsonify({'service': 'database-service',
            'status': 'healthy',
            'entries': len(DATA),
            'timestamp': datetime.datetime.now().isoformat()
            })

if __name__ == '__main__':
    # port muss mit dem port aus der kubernetes deployment yaml übereinstimmen
    app.run(host='0.0.0.0', port=5002)