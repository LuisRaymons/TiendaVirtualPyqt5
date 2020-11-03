from config import Conexion
from datetime import datetime
class PromotorModel:
    def __init__(self):
        self.con = Conexion.Conexion()
        self.conectar=self.con.conexion()

    def consultarColumnas(self):
    	try:
    		
    		sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='promotor' AND table_schema='tiendavirtual'"
    		self.conectar[3].execute(sql)
    		tablaColumnName = self.conectar[3].fetchall()

    		sql2 = "SELECT count(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'promotor' AND table_schema='tiendavirtual'"
    		self.conectar[3].execute(sql2)
    		totalColumns = self.conectar[3].fetchone()

    		sql3 = "SELECT * FROM tiendavirtual.promotor"
    		self.conectar[3].execute(sql3)
    		categorias = self.conectar[3].fetchall()

    		sql4 = "SELECT count(*) FROM tiendavirtual.promotor"
    		self.conectar[3].execute(sql4)
    		categoriasCount = self.conectar[3].fetchone()

    		valores =("success", 200, tablaColumnName, totalColumns, categorias,categoriasCount)

    	except Exception as e:
    		valores =("error", 500, '' , '', '', '')
    	return valores

    def store(self,data):
        try:
            sql = "INSERT INTO tiendavirtual.promotor(nombre,direccion,telefono,sitioWeb,created_at,updated_at) VALUES('"+data[0]+"','"+data[1]+"','"+data[2]+"','"+data[3]+"', '"+ str(datetime.now())+"', '"+str(datetime.now())+"')"
            retornPromo=self.conectar[3].execute(sql)
            self.conectar[2].commit()
            if(retornPromo == 1):
                valor = ("success", 200, data)
            else:
                valor = ("warning", 300, "Ocurrio un error al intentar guardar al promotor")
        except Exception as e:
            valor = ("error", 500, e)
        return valor