import pymysql
from config import Variable_entorno as configVar


class Conexion:

	def conexion(self):
		try:
			#self.connection = pymysql.connect( host='localhost', user='root', password='', db='tiendavirtual')
			self.connection = pymysql.connect(host=configVar.HOST,user=configVar.USER,password=configVar.PASSWORD,db=configVar.DB)
			self.cursor = self.connection.cursor()
			self.valores =("success", 200,self.connection,self.cursor)
		except Exception as e:
			self.valores =("error",500)
		return self.valores
	def closeconexion(self):
			self.connection.close()
			self.cursor.close()

			
		