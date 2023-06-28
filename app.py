from flask import Flask,  render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL,MySQLdb 
from os import path 
from notifypy import Notify


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'greensoftworld'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('contenido.html')

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        id_usu = request.form['id_usu']
        password = request.form['id_usu']
        

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM registro")
        registro = cur.fetchone()
        cur.close()

        if len(registro)==0 or len(registro)>0:
            if (id_usu == registro['id_usu']) and (email == registro['email']) and (password == registro['password']):
                return render_template("contenido.html")
                
            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        
        return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tipo_id")
    tipo = cur.fetchall()
    
    cur.close()
        
    notificacion = Notify()
    
    if request.method == 'GET':
        return render_template("registro.html",tipo = tipo)
    
    else:
        name = request.form['name']
        last_name = request.form['last_name']
        id_documento = request.form['tipo']
        id_usu = request.form['id_usu']
        email = request.form['email']
        password = request.form['password']
        celular = request.form['celular']  
            
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registro(name, email, password,last_name,celular,id_usu,id_documento) VALUES (%s,%s,%s,%s,%s,%s,%s)", (name, email, password,last_name,celular,id_usu,id_documento))
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="ya te encuentras registrado, por favor inicia sesión."
        return redirect(url_for('login'))
        


if __name__ == '__main__':
    app.run(debug=True)
    