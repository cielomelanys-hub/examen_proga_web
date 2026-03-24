import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS restaurante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            eslogan TEXT,
            descripcion TEXT NOT NULL,
            logo TEXT,
            imagen_portada TEXT
        );

        CREATE TABLE IF NOT EXISTS menu_almuerzo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            nombre_plato TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen TEXT,
            disponible TEXT NOT NULL
        );
    ''')

    existing = cursor.execute('SELECT COUNT(*) FROM restaurante').fetchone()[0]
    if existing == 0:
        cursor.execute('''
            INSERT INTO restaurante (nombre, eslogan, descripcion, logo, imagen_portada)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'Sabor Boliviano',
            'Almuerzos caseros con tradición',
            'Restaurante especializado en comida típica boliviana, ofreciendo almuerzos completos con ingredientes frescos y atención rápida.',
            'img/logo.png',
            'img/portada.jpg'
        ))

        menu_items = [
            ('2026-03-22', 'Sopa de maní', 'Sopa tradicional boliviana con fideo, papa y carne.', 'Entrada', 8.50, 'img/sopa_mani.jpg', 'Sí'),
            ('2026-03-22', 'Silpancho', 'Carne apanada con arroz, papa, huevo y ensalada.', 'Plato principal', 18.00, 'img/silpancho.jpg', 'Sí'),
            ('2026-03-22', 'Fricase paceño', 'Plato típico con carne de cerdo, mote y ají amarillo.', 'Plato principal', 20.00, 'img/fricase.jpg', 'Sí'),
            ('2026-03-22', 'Mocochinchi', 'Refresco tradicional frío de durazno deshidratado.', 'Bebida', 4.00, 'img/mocochinchi.jpg', 'Sí'),
            ('2026-03-22', 'Jugo de tumbo', 'Bebida natural refrescante.', 'Bebida', 5.00, 'img/jugo_tumbo.jpg', 'Sí'),
            ('2026-03-22', 'Flan casero', 'Postre suave preparado artesanalmente.', 'Postre', 6.00, 'img/flan.jpg', 'Sí'),
            ('2026-03-23', 'Sopa de verduras', 'Sopa ligera con verduras frescas.', 'Entrada', 7.50, 'img/sopa_verduras.jpg', 'Sí'),
            ('2026-03-23', 'Pollo al horno', 'Pollo dorado con papas y ensalada.', 'Plato principal', 17.00, 'img/pollo_horno.jpg', 'Sí'),
            ('2026-03-23', 'Refresco de linaza', 'Bebida natural digestiva.', 'Bebida', 3.50, 'img/linaza.jpg', 'Sí'),
            ('2026-03-23', 'Gelatina', 'Postre ligero de frutas.', 'Postre', 5.00, 'img/gelatina.jpg', 'Sí'),
        ]
        cursor.executemany('''
            INSERT INTO menu_almuerzo (fecha, nombre_plato, descripcion, categoria, precio, imagen, disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', menu_items)

    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()

    restaurante = conn.execute('SELECT * FROM restaurante LIMIT 1').fetchone()

    fecha_menu = '2026-03-22'
    menu = conn.execute(
        'SELECT * FROM menu_almuerzo WHERE fecha = ?', (fecha_menu,)
    ).fetchall()

    conn.close()

    return render_template('index.html', restaurante=restaurante, menu=menu, fecha=fecha_menu)


if __name__ == "__main__":
    ##app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)