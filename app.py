from sqlite3 import Cursor
from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin



app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = 'remotemysql.com' #env.getEnv("")
app.config['MYSQL_USER'] = 'FVJpgw76FR'
app.config['MYSQL_PASSWORD'] = '0uDPWv3khs'
app.config['MYSQL_DB'] = 'FVJpgw76FR'


conexion = MySQL(app)

@app.route('/')
def index():
    return ( 
    '<h1>Bienvenido a la API de la tienda</h1>'
    '<h2>Para ver los productos disponibles, ingresa a la ruta /productos con metodo get</h2>'
    '<h2>Para ver el detalle de cada producto, ingresa a la ruta /productos/id con metodo get</h2>'
    '<h2>Para agregar un producto, ingresa a la ruta /productos con metodo post</h2>'
    '<h2>Para actualizar un producto, ingresa a la ruta /productos/id con metodo put</h2>'
    '<h2>Para eliminar un producto, ingresa a la ruta /productos/id con metodo delete</h2>'
    )

@cross_origin
@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        cursor=conexion.connection.cursor()
        sql_query = 'SELECT * FROM productos'
        cursor.execute(sql_query)
        datos = cursor.fetchall()
        productos = []
        for producto in datos:
            producto = {
                'id': producto[0],
                'nombre': producto[1],
                'categoria': producto[2],
                'precio': producto[3],
                'descripcion': producto[4], 
                'imagen': str(producto[5])

            }
            productos.append(producto)
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)})

@cross_origin
@app.route('/productos/<id>', methods=['GET'])
def ver_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql_query = "SELECT * FROM productos WHERE producto_id = {0}".format(id)
        cursor.execute(sql_query)
        datos = cursor.fetchone()
        if datos != None:
            producto = {
                'id': datos[0],
                'nombre': datos[1],
                'categoria': datos[2],
                'precio': datos[3],
                'descripcion': datos[4],
                'imagen': str(datos[5])
            }
            return jsonify(producto)
        else:
            return jsonify({'mensaje': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'error': str(e)})


@cross_origin
@app.route('/productos', methods=['POST'])
def agregar_producto():
    try:
        cursor = conexion.connection.cursor()
        sql_query = """INSERT INTO productos 
        (nombre_producto, categoria_producto, precio_producto, descripcion_producto, imagen_producto)
        VALUES ('{0}', '{1}', {2}, '{3}', '{4}')""".format(
            request.json['nombre'], 
            request.json['categoria'], 
            request.json['precio'], 
            request.json['descripcion'],
            request.json['imagen']
        )
        cursor.execute(sql_query)
        conexion.connection.commit()#esto confirma los cambios que se van a agregar
        return jsonify({'mensaje': 'Producto agregado'})
    except Exception as e:
        return jsonify({'error': str(e)})

@cross_origin
@app.route('/productos/<id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql_query = "DELETE FROM productos WHERE producto_id = {0}".format(id)
        cursor.execute(sql_query)
        conexion.connection.commit()#esto confirma los cambios que se van a agregar
        return jsonify({'mensaje': 'Producto eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)})

@cross_origin
@app.route('/productos/<id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql_query = """UPDATE productos 
        SET nombre_producto = '{0}', 
        categoria_producto = '{1}', 
        precio_producto = {2}, 
        descripcion_producto = '{3}',
        imagen_producto = '{4}'
        WHERE producto_id = {5}""".format(
            request.json['nombre'], 
            request.json['categoria'], 
            request.json['precio'], 
            request.json['descripcion'],
            request.json['imagen'],
            id
        )
        cursor.execute(sql_query)
        conexion.connection.commit()#esto confirma los cambios que se van a agregar
        return jsonify({'mensaje': 'Producto actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)})

def pagina_no_encontrada(error):
    return '<h1>La pagina que estas buescando no existe</h1>', 404

if __name__ == '__main__':
    # app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)