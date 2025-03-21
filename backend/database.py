import mysql.connector
import logging

# Configuración de logging para registrar errores
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_db_connection():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="easygenapp"
        )
        logging.info("Conexión a MySQL establecida correctamente.")
        return conexion
    except mysql.connector.Error as e:
        logging.error(f"Error al conectar a MySQL: {e}")
        return None

# Crear las tablas si no existen
def crear_tablas():
    conexion = get_db_connection()
    if conexion:
        try:
            cursor = conexion.cursor()
            query_usuarios = '''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
            
            query_codigos = '''
            CREATE TABLE IF NOT EXISTS codigos_generados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                descripcion TEXT NOT NULL,
                codigo TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
            '''
            
            cursor.execute(query_usuarios)
            cursor.execute(query_codigos)
            conexion.commit()
            cursor.close()
            conexion.close()
            logging.info("Tablas creadas/verificadas correctamente.")
        except Exception as e:
            logging.error(f"Error al crear las tablas: {e}")

# Ejecutar la creación de las tablas al iniciar
crear_tablas()
