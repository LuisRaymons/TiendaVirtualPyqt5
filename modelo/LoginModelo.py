import sys
from config import Conexion as con

class LoginModelo():
	def __init__(self):
		self.conex=con.Conexion()
		self.conectar=self.conex.conexion()

	def getUser(self,v_id):
		
		try:
			sql = "SELECT * FROM tiendavirtual.users u JOIN tiendavirtual.model_has_roles mhr ON(u.id=mhr.model_id) JOIN tiendavirtual.roles r ON(mhr.role_id=r.id) WHERE u.id=" +  str(v_id) 
			self.conectar[3].execute(sql)
			UserLogin = self.conectar[3].fetchall()
			valores =("success", 200,UserLogin)
		except Exception as e:
			valores =("success", 200, e)
		return valores

	def getUserFace(self, nombre):
		try:
			sql  = "SELECT * FROM tiendavirtual.users WHERE name='" + str(nombre) + "'"
			self.conectar.execute(sql)
			user = self.conectar[3].fetchone()
			valores =("success", 200,user)
		except Exception as e:
			valores =("success", 200, e)
		return valores


