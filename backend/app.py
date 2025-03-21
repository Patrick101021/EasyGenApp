
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import google.generativeai as genai
import config
import os
import hashlib
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración MySQL
conexion = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = conexion.cursor(dictionary=True)

# Configuración Google Gemini AI
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def hash_password(password):
    salt = os.urandom(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return f"scrypt:16384:8:1${base64.b64encode(salt).decode()}${key.hex()}"

def verify_scrypt_password(stored_hash, password):
    try:
        parts = stored_hash.split("$")
        if len(parts) != 3:
            print("⚠️ Formato de hash inválido:", stored_hash)
            return False

        params, salt_b64, stored_key_hex = parts
        n, r, p = map(int, params.replace("scrypt:", "").split(":"))
        salt = base64.b64decode(salt_b64)
        new_key = hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p)
        return new_key.hex() == stored_key_hex
    except Exception as e:
        print(f"❌ Error al verificar contraseña: {e}")
        return False


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not all([nombre, email, password]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)", 
                       (nombre, email, hashed))
        conexion.commit()
        return jsonify({'mensaje': 'Usuario registrado con éxito'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Correo y contraseña requeridos'}), 400

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and verify_scrypt_password(user['password_hash'], password):
        return jsonify({'mensaje': 'Login exitoso'})
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/generar_codigo', methods=['POST'])
def generar_codigo():
    data = request.json
    descripcion = data.get('descripcion')
    if not descripcion:
        return jsonify({'error': 'Descripción requerida'}), 400

    try:
        # Prompt más abierto y flexible
        prompt = f"Eres un generador experto de código. Genera el código correspondiente a la siguiente descripción: {descripcion}"

        respuesta = model.generate_content(prompt)
        return jsonify({'codigo': respuesta.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
