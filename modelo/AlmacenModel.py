from config import Conexion
from datetime import datetime
class ALmacenModel:
    def __init__(self):
        self.con = Conexion.Conexion()
        self.conectar=self.con.conexion()

    def consultarColumnas(self):
    	try:
    		
    		sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='almacen' AND table_schema='tiendavirtual'"
    		self.conectar[3].execute(sql)
    		tablaColumnName = self.conectar[3].fetchall()

    		sql2 = "SELECT count( COLUMN_NAME ) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'almacen' AND table_schema='tiendavirtual'"
    		self.conectar[3].execute(sql2)
    		totalColumns = self.conectar[3].fetchone()

    		sql3 = "SELECT * FROM tiendavirtual.almacen"
    		self.conectar[3].execute(sql3)
    		categorias = self.conectar[3].fetchall()

    		sql4 = "SELECT count(*) FROM tiendavirtual.almacen"
    		self.conectar[3].execute(sql4)
    		categoriasCount = self.conectar[3].fetchone()

    		valores =("success", 200, tablaColumnName, totalColumns, categorias,categoriasCount)

    	except Exception as e:
    		valores =("error", 500, '' , '', '', '')
    	return valores
    def store(self,data1,data2):

        try:
            sqlUser = "SELECT * FROM tiendavirtual.users WHERE name='" + str(data2) + "'"
            self.conectar[3].execute(sqlUser)
            user = self.conectar[3].fetchone()

            sqlProduct = "SELECT * FROM tiendavirtual.producto WHERE nombre='" +data1[3]+ "'"
            self.conectar[3].execute(sqlProduct)
            product = self.conectar[3].fetchone()

            sql="INSERT INTO tiendavirtual.almacen(folio,imgFolio,entrada,salida,stock,id_user,id_producto,created_at,updated_at) VALUES('"+data1[0]+"','"+data1[2]+"',"+str(data1[1])+", 0, "+str(data1[1])+","+str(user[0])+","+str(product[0])+", '"+str(datetime.now())+"','"+str(datetime.now())+"')"
            almacen = self.conectar[3].execute(sql)
            self.conectar[2].commit()

            if(almacen == 1):
                valor=("success",200,data1)
            else:
                valor=("warning", 300, "Error al insertar almacen")
        except Exception as e:
            valor=("error", 500,e)

        return valor