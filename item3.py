from flask import Flask, request, jsonify
import sqlite3
import keyring
import bcrypt

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

#Ruta raiz
@app.route('/')
def index():
    return "El servidor Flask está funcionando", 200

# Ruta para añadir un usuario
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Hash de la contraseña utilizando bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Guardar la clave utilizando keyring
    keyring.set_password('my_app', username, hashed_password.decode('utf-8'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password.decode('utf-8')))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuario agregado'}), 201

# Ruta para validar un usuario
@app.route('/validate_user', methods=['POST'])
def validate_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return jsonify({'message': 'Usuario validado'}), 200
        else:
            return jsonify({'message': 'Credenciales invalidas'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify(users), 200

if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=5800)
