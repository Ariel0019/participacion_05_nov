from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crear la base de datos y la tabla si no existen
def init_db():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Ruta para mostrar todos los productos
@app.route('/')
def index():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM producto')
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/add', methods=['POST'])
def add_product():
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)', 
                   (descripcion, int(cantidad), float(precio)))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Ruta para mostrar el formulario de edición
@app.route('/edit/<int:id>')
def edit_product(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM producto WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('edit.html', producto=producto)

# Ruta para actualizar un producto
@app.route('/update/<int:id>', methods=['POST'])
def update_product(id):
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?
    ''', (descripcion, int(cantidad), float(precio), id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Ruta para eliminar un producto
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
