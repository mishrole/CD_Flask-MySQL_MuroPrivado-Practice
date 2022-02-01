import pymysql.cursors

class MySQLConnection:
    def __init__( self, database):
        connection = pymysql.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'mysql',
            db = database,
            port = 3306,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
    
        # Establece la conexión a la base de datos
        self.connection = connection

    # Consultar base de datos
    def query_db( self, query, data = None ):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify( query, data )
                print('Running query:', query)

                cursor.execute( query, data )

                if query.lower().find("insert") >= 0:
                    # Consultas INSERT devolverán el número de Id de la fila insertada
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # Consultas SELECT devolverán los datos como una Lista de diccionarios
                    result = cursor.fetchall()
                    return result
                else:
                    # Las consultas UPDATE y DELETE no devolverán nada
                    self.connection.commit()
            except Exception as ex:
                # Si la consulta falla, el método retorna False
                print("Something went wrong:", ex)
                return False
            finally:
                # Cerrar la conexión a la base de datos
                self.connection.close()
    
# Recibe la base de datos que estamos usando y la usa para crear una instancia de MySQLConnection
def connectToMySQL( database ):
    return MySQLConnection( database )