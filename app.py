import requests
from flask import Flask , render_template, request , redirect , url_for, flash, jsonify
from flask_mysqldb import MySQL
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from cloudinary.utils import cloudinary_url





load_dotenv()


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jevil'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'
mysql = MySQL(app)

app.secret_key= 'pruebakey'



CORS(app)
logging.basicConfig(level=logging.DEBUG)
#verify cloud
app.logger.info('%s',os.getenv('CLOUD_NAME'))




        



"""

-------------------CITIES-------------------

"""

@app.route('/cities', methods=['GET'])
def cites():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cities')
    data = cur.fetchall()
    info = []
    for city in data:
        informacio ={'id':city[0],'code':city[1],'name':city[2]}
        info.append(informacio)
    return jsonify({'cities':info})

@app.route('/cities/<string:id>', methods=['GET'])
def citiesid (id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cities WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return jsonify({'cities':data[0]})




@app.route('/citiesPost', methods=['POST'])
def citiePost():
    if request.method == 'POST':
        code = request.json['code']
        name = request.json['name']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cities (code, name) VALUES (%s, %s)', (code, name))
        mysql.connection.commit()
        return jsonify({'message': 'City Added Succesfully'})


@app.route('/citiesPut/<string:id>', methods=['PUT'])
def citiePut(id):
    if request.method == 'PUT':
        code = request.json['code']
        name = request.json['name']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE cities
            SET code = %s,
                name = %s
            WHERE id = %s
        """, (code, name, id))
        mysql.connection.commit()
        return jsonify({'message': 'City Updated Succesfully'})



@app.route('/citiesDelete/<string:id>', methods=['DELETE'])
def citieDeles(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cities WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return jsonify({
            'message': 'Product Deleted',
        })



"""

-------------------ENDCITIES-------------------

"""


#---------------------------------------------------------------------


"""

-------------------Clients-------------------

"""

@app.route('/clients', methods=['GET'])
def clients():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clients')
    data = cur.fetchall()
    info = []
    for client in data:
        informacio ={'id':client[0],'code':client[1],'name':client[2], 'city':client[3]}
        info.append(informacio)
    return jsonify({'cities':info})


@app.route('/clients/<string:id>', methods=['GET'])
def clientsid (id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clients WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return jsonify({'clients':data[0]})


@app.route('/clientscity/<string:city>', methods=['GET'])
def clientscity (city):
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clients WHERE city = '{0}' ".format(city))
    data = cur.fetchall()
    return jsonify({'clients':data[0]})





@app.route('/clientsPost', methods=['POST'])
def clientsPost():
    if request.method == 'POST':
        code = request.json['code']
        name = request.json['name']
        city = request.json['city']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clients (code, name, city) VALUES (%s, %s, %s)', (code, name, city))
        mysql.connection.commit()
        return jsonify({'message': 'Clint Added Succesfully'})


@app.route('/clientsPut/<string:id>', methods=['PUT'])
def clientsPut(id):
    if request.method == 'PUT':
        code = request.json['code']
        name = request.json['name']
        city = request.json['city']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clients
            SET code = %s,
                name = %s,
                city = %s
            WHERE id = %s
        """, (code, name,city, id))
        mysql.connection.commit()
        return jsonify({'message': 'City Updated Succesfully'})


@app.route('/clientsDelete/<string:id>', methods=['DELETE'])
def clientsDeles(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clients WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return jsonify({
            'message': 'Product Deleted',
        })


"""

-------------------EndClients-------------------

"""


#---------------------------------------------------------------------


"""

-------------------Users-------------------

"""


@app.route('/users', methods=['GET'])
def users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    info = []
    for user in data:
        informacio ={'id':user[0],'name':user[1], 'pass':user[2],'email':user[3], 'phot':user[4]}
        info.append(informacio)
    return jsonify({'users':info})


@app.route('/users/<string:id>', methods=['GET'])
def usersid (id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM  users  WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return jsonify({'clients':data[0]})



@app.route('/usersPost', methods=['POST'])
@cross_origin()
def usersPost():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        app.logger.info(type(upload_result))
        url = upload_result['url']
        
        name = request.form.get("name")
        password = request.form.get("pass")
        email = request.form.get("email")
        photo = url
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (name, pass, email, photo) VALUES (%s, %s, %s, %s)', (name, password, email, photo))
        mysql.connection.commit()
        mysql.connection.commit()
        return jsonify({'message': 'User Added Succesfully'})


@app.route('/usersPut/<string:id>', methods=['PUT'])
def usersPut(id):
    app.logger.info('in upload route')
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == 'PUT':
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        app.logger.info(type(upload_result))
        url = upload_result['url']
        
        name = request.form.get("name")
        password = request.form.get("pass")
        email = request.form.get("email")
        photo = url
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name = %s,
                pass = %s,
                email = %s,
                photo = %s
            WHERE id = %s
        """, (name,password, email, photo, id))
        mysql.connection.commit()
        return jsonify({'message': 'User Updated Succesfully'})


@app.route('/usersDelete/<string:id>', methods=['DELETE'])
def usersDeles(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return jsonify({
            'message': 'User Deleted',
        })



"""

-------------------EndUsers-------------------

"""


#---------------------------------------------------------------------



"""

--------------------------Templates

"""



@app.route('/city')
def city():
    response = requests.get("http://127.0.0.1:3000/cities")
    data = response.json()
    print(data)
    return render_template("city.html", cities=data)


@app.route('/cityPost', methods=['POST'])
def cityPost():
    code = request.form['code']
    name = request.form['city']
    response = requests.post('http://127.0.0.1:3000/citiesPost', json={'code': code, 'name': name})
    if response.status_code == 200:
        return 'Formulario enviado con éxito'
    else:
        return 'Error al enviar el formulario'



@app.route('/client')
def client():
    response = requests.get("http://127.0.0.1:3000/clients")
    data = response.json()
    print(data)
    return render_template("client.html",cities=data)


@app.route('/clientPost', methods=['POST'])
def clientPost():
    code = request.form['code']
    name = request.form['name']
    city = request.form['city']
    response = requests.post('http://127.0.0.1:3000/clientsPost', json={'code': code, 'name': name , 'city': city })
    if response.status_code == 200:
        return 'Formulario enviado con éxito'
    else:
        return 'Error al enviar el formulario'



@app.route('/user', methods=['GET'])
def user():
    response = requests.get("http://127.0.0.1:3000/users")
    data = response.json()
    
    
    email=  data['users'][0]['email']
    name = data['users'][0]['name']
    password = data['users'][0]['pass']
    url = data['users'][0]['phot']
    
    
    print(url)
    return render_template("user.html",cities = data ,email=email, url=url, name=name, password=password)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    
    
