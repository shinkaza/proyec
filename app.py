from flask import Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cliente"
    )

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['Usuario']
        Contraseña = request.form['Contraseña']
        cedula = request.form['cedula']
        categoria = request.form['categoria']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cliente (nombre, apellido,cedula ,usuario,categoria,Contraseña) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nombre, apellido,cedula,usuario,categoria,Contraseña))
            us=cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            print(us)
            return render_template('register.html')
        except Error as e:
            print("Error al registrar:", e)
            return "Error al registrar usuario"
    return render_template('register.html')

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        Contraseña = request.form['Contraseña']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente WHERE usuario=%s AND Contraseña=%s", (usuario, Contraseña))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
                session['usuario'] = user['usuario']
                session['categoria'] = user['categoria']
        if user['categoria'] == 'admin':
                return redirect('/admin')
        else:
                return redirect('/user')
    else:
        return render_template('login.html')
    


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if session.get('categoria') != 'admin':
        return "Acceso denegado"

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        id = request.form['id']
        cursor.execute("INSERT INTO items (nombre, descripcion,id) VALUES (%s,%s,%s)", (name, desc,id))
        conn.commit()

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('admin_temp.html', items=items)



@app.route('/update', methods=['GET', 'POST'])
def update():
    if session.get('categoria') != 'admin':
        return "Acceso denegado"

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        id = request.form['id']
        cursor.execute("UPDATE nombre, descripction SET (%s,%s) WHERE id=%s",(name,desc,id))
        conn.commit()

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('admin_temp.html', items=items)

    



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('categoria') != 'admin':
        return "Acceso denegado"

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        id = request.form['id']
        cursor.execute("DELETE FROM items WHERE id=%s", (id))
        conn.commit()

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('admin_temp.html', items=items)


@app.route('/user')
def user():
    if session.get('categoria') != 'usuario':
        return "Acceso denegado"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('dashboar.html', items=items)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



@app.route('/search')
def search():
     return render_template('buscar.html')


@app.route('/updat')
def updat():
     return render_template('update.html')


@app.route('/update2')
def update2():
     return render_template('update2.html')



if __name__ == '__main__':
    app.run(debug=True)
