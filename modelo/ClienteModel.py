from config import Conexion
from datetime import datetime
class ClienteModel:
    def __init__(self):
        self.con = Conexion.Conexion()
        self.conectar = self.con.conexion()
        self.now = datetime.now()
    def consultarColumnas(self, inicio, fin):
    	try:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='cliente' AND table_schema='tiendavirtual'"
            self.conectar[3].execute(sql)
            tablaColumnName = self.conectar[3].fetchall()
            sql2 = "SELECT count( COLUMN_NAME ) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'cliente' AND table_schema='tiendavirtual'"
            self.conectar[3].execute(sql2)
            totalColumns = self.conectar[3].fetchone()
            sql3 = "SELECT * FROM tiendavirtual.cliente limit 50"
            self.conectar[3].execute(sql3)
            categorias = self.conectar[3].fetchall()

            sql4 = "SELECT count(*) FROM tiendavirtual.cliente"
            self.conectar[3].execute(sql4)
            categoriasCount = self.conectar[3].fetchone()

            valores =("success", 200, tablaColumnName, totalColumns, categorias,categoriasCount)
    	except Exception as e:
    		valores =("error", 500, '' , '', '', '')
    	return valores
    def getColonia(self):
        try:
            sql = "SELECT * FROM tiendavirtual.colonia"
            self.conectar[3].execute(sql)
            tablaColonia = self.conectar[3].fetchall()
            colonias = ("success", 200, tablaColonia)
        except Exception as e:
            colonias = ("success", 200, e)
        return colonias
    def store(self, data):
        try:
            sqlConsul = "SELECT id FROM  tiendavirtual.colonia WHERE nombre='" + data[4]+ "'" #
            self.conectar[3].execute(sqlConsul)
            idColonia = self.conectar[3].fetchone()
            sql = "INSERT INTO tiendavirtual.cliente(nombre,apellidos,telefono,direccion,id_colonia,created_at) VALUES('" + data[0] +"','"+data[1]+"','"+data[2]+"','"+data[3]+"', " + str(idColonia[0]) + ",'" + str(self.now) + "')"

            retornoClient=self.conectar[3].execute(sql)
            self.conectar[2].commit()
            self.con.closeconexion()

            if(retornoClient == 1):
                valor = ("success", 200, data)
            else:
                valor = ("warning", 400, "No se pudo insertar cliente")
        except Exception as e:
            valor = ("error", 500, e)
        return valor
    def consultarColonia(self, idcolonia):
        
        try:
            sql = "SELECT * FROM tiendavirtual.colonia WHERE id = " + str(idcolonia)
            self.conectar[3].execute(sql)
            colonia = self.conectar[3].fetchone()
            coloniaSelected = ("success", 200, colonia)
        except Exception as e:
            coloniaSelected = ("error", 500, e)
        return coloniaSelected
    def update(self, data):
        try:
            if(data[5]=='Seleccione una colonia'):
                self.colonia=0
            else:
                self.colonia=data[5]

            if(self.colonia != 0):
                sqlCol = "SELECT * FROM tiendavirtual.colonia WHERE nombre = '" + str(self.colonia) + "'"
                self.conectar[3].execute(sqlCol)
                col = self.conectar[3].fetchone()
                sql="UPDATE tiendavirtual.cliente SET nombre='"+data[1]+"',apellidos='"+data[2]+"',telefono='"+data[3]+"',direccion='"+data[4]+ "',updated_at='" +str(self.now)+ "', id_colonia=" + str(col[0]) + " WHERE id="+ str(data[0])
            else:
                sql="UPDATE tiendavirtual.cliente SET nombre='"+data[1]+"',apellidos='"+data[2]+"',telefono='"+data[3]+"',direccion='"+data[4]+ "',updated_at='" +str(self.now)+ "' WHERE id="+ str(data[0])
            self.conectar[3].execute(sql)
            self.conectar[2].commit()
            sqlConsulCli = "SELECT * FROM tiendavirtual.cliente WHERE id=" + str(data[0])
            self.conectar[3].execute(sqlConsulCli)
            cliente = self.conectar[3].fetchone()
            valor=("success", 200, cliente)
        except Exception as e:
            valor=("error", 50, e)
        return valor
    def destroy(self, id):
        try:
            sql = "DELETE FROM tiendavirtual.cliente WHERE id=" + str(id)
            self.conectar[3].execute(sql)
            self.conectar[2].commit()
            valor=("success", 200, id)
        except Exception as e:
            valor=("error", 500, e)
        return valor
        



'''

nombre
apellidos
telefono
direccion
id_colonia

'''