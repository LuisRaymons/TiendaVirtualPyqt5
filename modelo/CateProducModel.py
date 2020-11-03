from config import Conexion
from datetime import datetime
class CateProducModel:
	def __init__(self):
		self.con = Conexion.Conexion()
		self.conectar=self.con.conexion()

	def consultarColumnas(self):
		try:
			
			sql = "CALL sp_categoria_producto(0,'','COLUMNS')"
			self.conectar[3].execute(sql)
			tablaColumnName = self.conectar[3].fetchall()

			
			sql2 = "CALL sp_categoria_producto(0,'','COUNTCOLUMN')"
			self.conectar[3].execute(sql2)
			totalColumns = self.conectar[3].fetchone()
			
			sql3 = "CALL sp_categoria_producto(0,'','READ')"
			self.conectar[3].execute(sql3)
			categorias = self.conectar[3].fetchall()

			sql4 = "CALL sp_categoria_producto(0,'','COUNTDATA')"
			self.conectar[3].execute(sql4)
			categoriasCount = self.conectar[3].fetchone()
			#print(categoriasCount)

			valores =("success", 200, tablaColumnName, totalColumns, categorias,categoriasCount)


		except Exception as e:
			valores =("error", 500, '' , '', '', '')
		return valores
	def store(self, nombre):
		try:
			sqlexist = "CALL sp_categoria_producto(0,%s,'COUNTEXIST')"
			valexist  = (str(nombre))
			cateexist = self.conectar[3].execute(sqlexist,valexist)
			totalcateexists = self.conectar[3].fetchone()		

			if(totalcateexists[0]==0):
				consultCate = "CALL sp_categoria_producto(0,%s,'CREATE')"
				val = (str(nombre))
				retornCate = self.conectar[3].execute(consultCate,val)
				self.conectar[2].commit()
				if(retornCate == 1):
					valor = ("succes",200,nombre)
				else:
					valor = ("warning", 300, "Ocurrio un error al intentar guardar la categoria del producto")
			else:
				valor = ("warning", 202, "Registro ya existe")
		except Exception as e:
			valor = ("error", 500, e)
		return valor
	def update(self,data):
		try:

			sql = "CALL sp_categoria_producto(%s,%s,'UPDATE')"
			val  = (data[0],data[1])			
			catego = self.conectar[3].execute(sql,val)
			self.conectar[2].commit()

			if(catego == 1):
				valor = ("success", 200, data)
			else:
				valor = ("warning",  300, "Erro en la modificacion del catalogo")
		except Exception as e:
			valor = ("error", 500, e)
		return valor
	def destroy(self,data):
		try:
			sql = "CALL sp_categoria_producto(%s,'','DELETE')"
			val  = (data[0])

			catego = self.conectar[3].execute(sql,val)
			self.conectar[2].commit()

			if(catego == 1):
				valor = ("success", 200, data)
			else:
				valor = ("warning", 300, "El registro no fue eliminado")
		except Exception as e:
			valor = ("error", 500, e)
		return valor