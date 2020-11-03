from config import Conexion
from datetime import datetime

class VentaModel:
	def __init__(self):
		self.con = Conexion.Conexion()
		self.conectar=self.con.conexion()

	def consultarColumnas(self):
		try:
			sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='venta' AND table_schema='tiendavirtual'"
			self.conectar[3].execute(sql)
			tablaColumnName = self.conectar[3].fetchall()

			sql2 = "SELECT count(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'venta' AND table_schema='tiendavirtual'"
			self.conectar[3].execute(sql2)
			totalColumns = self.conectar[3].fetchone()

			sql3 = "SELECT id,factura,impuesto,precio_total,tipoPago,id_cliente,id_users FROM tiendavirtual.venta"
			self.conectar[3].execute(sql3)
			venta = self.conectar[3].fetchall()

			sql4 = "SELECT count(*) FROM tiendavirtual.venta"
			self.conectar[3].execute(sql4)
			ventaCount = self.conectar[3].fetchone()

			valores =("success", 200, tablaColumnName, totalColumns, venta,ventaCount)


		except Exception as e:
			valores =("error", 500, '' , '', '', '')
		return valores

	def getClient(self):
		try:
			sql = "SELECT * FROM tiendavirtual.cliente"
			self.conectar[3].execute(sql)
			clientes = self.conectar[3].fetchall()
			valor = ("success", 200, clientes)

		except Exception as e:
			valor = ("error", 500, e)
		return valor

	def store(self,data):
		try:
			sqlclient = "SELECT * FROM tiendavirtual.cliente WHERE nombre='"+data[4]+"'"
			self.conectar[3].execute(sqlclient)
			client = self.conectar[3].fetchone()

			sqluser = "SELECT * FROM tiendavirtual.users WHERE name='"+data[5]+"' "
			self.conectar[3].execute(sqluser)
			user = self.conectar[3].fetchone()

			sql = "INSERT INTO tiendavirtual.venta(factura,impuesto,precio_total,tipoPago,id_cliente,id_users,created_at,updated_at) VALUES('"+data[0]+"',"+str(data[1])+", "+str(data[2])+",'"+data[3]+"', "+str(client[0])+","+str(user[0])+", '"+str(datetime.now())+"', '"+str(datetime.now())+"')"
			venta = self.conectar[3].execute(sql)
			self.conectar[2].commit()
			if(venta  == 1):
				valor = ("success", 200,data)
			else:
				valor = ("warning", 300, "Error al guardar la venta")

		except Exception as e:
			valor = ("error", 500, e)
		return valor