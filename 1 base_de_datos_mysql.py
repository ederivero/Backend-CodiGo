from MySQLdb import _mysql

conexion = _mysql.connect(host='localhost', user='root', password='root', database='pruebas')

conexion.query("SELECT * FROM usuarios;")

resultado = conexion.store_result()

print(resultado.fetch_row())