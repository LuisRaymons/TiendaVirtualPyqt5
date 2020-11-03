from PyQt5.QtWidgets import *
from config import Conexion

from view import LoginView
from view.Errors import ErrorGeneral

class StarRuning:
	def __init__(self):
		con = Conexion.Conexion()
		error = ErrorGeneral.ErrorGeneral()
		conex=con.conexion()

		if(conex[0] == 'error'):
			error.messageError("Error 500","El servidor se encuentra apagado o esta en manteniemiento");
		elif(conex[0] == 'success'):
			lg = LoginView.LoginView()
			lg.LoginSearch()



if __name__ == "__main__":
	app = QApplication([])
	window = StarRuning()

	#app.exec_()
	sys.exit(app.exec_())



  