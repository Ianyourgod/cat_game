# WIP
from flask import Flask, request, jsonify

app = Flask(__name__)

rooms = []
# room layout: {name: str, players: [player], host: sid, started: bool}
# player layout: {username: str, x: int, y: int, direction: str}

@app.route('/join', methods=['POST'])
def join():
    data = request.get_json()
    username = data['name']
    room = data['room']
    for i in rooms:
        if i['name'] == room:
            if username in [j['username'] for j in i['players']]:
                return jsonify({'success': False, 'message': 'Username already taken.'})
            i['players'].append({'username': username, 'x': 0, 'y': 0, 'direction': 'N'})
            return jsonify({'success': True, 'message': 'Joined room.'})
        
@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    username = data['name']
    room = data['room']
    for i in rooms:
        if i['name'] == room:
            return jsonify({'success': False})
    rooms.append({'name': room, 'players': [{'username': username, 'x': 0, 'y': 0, 'direction': 'N'}], 'host': username, 'started': False})
    return jsonify({'success': True})

@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    return jsonify(rooms)

@app.route('/leave', methods=['POST'])
def leave():
    data = request.get_json()
    username = data['name']
    room = data['room']
    for i in rooms:
        if i['name'] == room:
            for j in i['players']:
                if j['username'] == username:
                    i['players'].remove(j)
                    return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Room not found.'})

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    username = data['name']
    room = data['room']
    for i in rooms:
        if i['name'] == room:
            for j in i['players']:
                if j['username'] == username:
                    j['x'] = data['x']
                    j['y'] = data['y']
                    j['direction'] = data['direction']
                    return jsonify({'success': True, 'players': i['players']})
    return jsonify({'success': False, 'message': 'Room not found.'})

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')