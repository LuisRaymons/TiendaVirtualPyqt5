from config import Conexion

class UserModel:
	def __init__(self):
		self.con = Conexion.Conexion()
		self.conectar=self.con.conexion()

	def consultarColumnas(self):
		try:
			
			sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='users' AND table_schema='tiendavirtual'"
			self.conectar[3].execute(sql)
			tablaColumnName = self.conectar[3].fetchall()

			sql2 = "SELECT count( COLUMN_NAME ) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'users' AND table_schema='tiendavirtual'"
			self.conectar[3].execute(sql2)
			totalColumns = self.conectar[3].fetchone()

			sql3 = "SELECT id,name,email,remember_token,created_at,updated_at FROM tiendavirtual.users"
			self.conectar[3].execute(sql3)
			users = self.conectar[3].fetchall()

			sql4 = "SELECT count(*) FROM tiendavirtual.users"
			self.conectar[3].execute(sql4)
			usersCount = self.conectar[3].fetchone()

			valores =("success", 200, tablaColumnName, totalColumns, users,usersCount)

		except Exception as e:
			valores =("error", 500, '' , '', '', e)
		return valores

	def getRole(self):
		try:
			sql = "SELECT * FROM tiendavirtual.roles"
			self.conectar[3].execute(sql)
			roles = self.conectar[3].fetchall()
			valor = ("success", 200, roles)
		except Exception as e:
			valor = ("error", 500, e)
		return valor

	def roles(self,iduser):
		try:
			sql="SELECT u.id,u.name,mr.*,r.name FROM users U JOIN model_has_roles mr ON(u.id = mr.model_id) JOIN roles r ON(mr.role_id=r.id) WHERE u.id=" + str(iduser)
			self.conectar[3].execute(sql)
			rol = self.conectar[3].fetchall()
			valor = ("success", 200, rol)
		except Exception as e:
			valor = ("error", 500, e)
		return valor