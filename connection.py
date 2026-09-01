import psycopg2
from pgvector.psycopg2 import register_vector

class base_de_datos:
    def __init__(self, data_base_host: str, data_base_name: str, data_base_user: str, data_base_password: str, data_base_port: int):
        self.connection = psycopg2.connect(
        host = data_base_host,
        dbname = data_base_name,
        user = data_base_user,
        password = data_base_password,
        port = data_base_port
        )
        register_vector(self.connection)
        self.cursor = self.connection.cursor()
    def create_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS propietario( idpropietario SERIAL PRIMARY KEY, nbpropietario VARCHAR(40), appropietario VARCHAR(40), cedula int UNIQUE, edificio int, apartamento CHAR(2), foto vector(128), cara TEXT)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS ON propietario USING hnsw (foto vector_cosine_ops);")
        except:
            pass
    def agregar_usuario(self, nombre: str, apellido: str, cedula: int, edificio: int, apartamento: str, foto, cara):
        try:
            self.cursor.execute("INSERT INTO propietario(nbpropietario,appropietario,cedula,edificio,apartamento,foto,cara) VALUES(%s,%s,%s,%s,%s,%s,%s);", (nombre,apellido,cedula,edificio,apartamento,foto,cara))
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except:
            pass
    def editar_usuario(self, nombre: str, apellido: str, cedula: int, cedula_anterior: int, edificio: int, apartamento: str):
        try:
            self.cursor.execute(f"UPDATE propietario SET nbpropietario = '{nombre}', appropietario = '{apellido}', cedula = {cedula}, edificio = {edificio}, apartamento = '{apartamento}' WHERE cedula = {cedula_anterior};")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except:
            pass
    def editar_photo(self,cedula: int, foto: str) -> None:
        try:
            self.cursor.execute("UPDATE propietario SET cara = %s WHERE cedula = %s;", (str(foto), cedula))
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except:
            pass
    def borrar_usuario(self, cedula: int):
        try:
            self.cursor.execute(f"DELETE FROM propietario WHERE cedula = {cedula};")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except:
            pass
    def buscar_usuario(self, cedula: int) -> list:
        try:
            self.cursor.execute(f"SELECT * FROM propietario WHERE cedula = {cedula}; ")
            regresar = self.cursor.fetchone()
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return regresar
        except:
            pass
    def comparar_caras(self, face_embedings) -> tuple:
        try:
            self.cursor.execute("SELECT cedula, (foto <=> %s) AS distance FROM propietario ORDER BY distance ASC LIMIT 1;", (face_embedings,))       
            regresar = self.cursor.fetchone()
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            if regresar and regresar[1] < 0.6:
                return regresar
            else:
                regresar[0] = 'No se detecto ninguna cara parecida en la base de datos'
                return regresar
        except psycopg2.Error as e:
            print(f"Error message: {e}")
            print(f"PostgreSQL Error Code: {e.pgcode}")
            print(f"{e.pgerror}")
            print(f"{e.cursor}")
            self.cursor.execute("ROLLBACK")
            self.connection.commit
            self.cursor.close()
            self.connection.close()
        
