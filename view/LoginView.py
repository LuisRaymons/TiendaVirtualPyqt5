from slugify import slugify 
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from controller import LoginController
from view import Principal
from view.Errors import ErrorGeneral
from moduloFace import CapturaRostro
from config import Variable_entorno as config
import sys
import requests
import json


class LoginView(QtWidgets.QMainWindow):
	def __init__(self):
		super(LoginView, self).__init__()
		self.LC=LoginController.LoginController()
		self.error = ErrorGeneral.ErrorGeneral()
		self.faceCapt = CapturaRostro.CapturaRostro()
		self.setStyleSheet(open('css/login.css').read())
	
	def LoginSearch(self):
		app = QApplication(sys.argv)
		self.LoginShowView = QWidget(None, QtCore.Qt.WindowCloseButtonHint)
		
		self.LoginShowView.setWindowTitle('Login LRVA')
		self.LoginShowView.setWindowIcon(QIcon('icon/tienda.png')) 
		self.LoginShowView.setGeometry(450,320,450,230)

		self.tabWidget = QtWidgets.QTabWidget(self.LoginShowView)
		_translate = QtCore.QCoreApplication.translate
		self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1265, 700))
		self.tabWidget.setObjectName("tabWidget")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.tabWidget.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")

		self.tabWidget.addTab(self.tab_2, "")
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Login"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Register"))

		login = self.loginvista(self.tab)
		register = self.loginregister(self.tab_2)
		
		

		self.LoginShowView.show()
		sys.exit(app.exec_())

	def check_password(self):
		
		self.session = self.LC.checkLoginC(self.txt_token.text())
		return self.session;
	
	def RoleSelect(self):
		users = self.check_password();
		self.role=list()
		self.nombre = "";

		for u in users[2]:
			self.role.append(u[12])
			self.nombre = u[1]

		if(len(self.role) > 1):
			value, ok = QInputDialog.getItem(self, "Roles", "Seleccione el tipo de usuario:", self.role)
			if(ok):
				self.LoginShowView.close()
				if(value == 'Administrador'):
					self.principal = Principal.Principal([self.nombre,value],self.LoginShowView)
					self.principal.show()
				elif(value == 'Ayudante'):
					self.principal = Principal.Principal([self.nombre,value],self.LoginShowView)
			else:
				self.error.messageError("Error 201","Rol no disponible");
				self.LoginShowView.show()
		elif(len(self.role) == 0):
			self.error.messageError("Error 403","Usuario no disponible");
			self.LoginShowView.show()
		elif(len(self.role) == 1):
			self.LoginShowView.close()
			self.principal = Principal.Principal([self.nombre,self.role],self.LoginShowView)
			self.principal.show()
		else:
			self.LoginShowView.show()

	def loginvista(self,tab):
		
		label_correo = QLabel("Correo: ",tab)
		label_correo.setGeometry(10,10,70,40)

		txt_correo = QLineEdit(tab)
		txt_correo.setPlaceholderText('Correo electronico')
		txt_correo.setGeometry(80,10,360,25)
		txt_correo.setFocus()

		label_password = QLabel("Contraseña: ", tab)
		label_password.setGeometry(10,50,70,40)

		passwordtxt = QLineEdit(tab)
		passwordtxt.setPlaceholderText('Contraseña de accesso')
		passwordtxt.setEchoMode(QLineEdit.Password)
		passwordtxt.setGeometry(80,50,360,25)

		button_login = QPushButton(tab)
		button_login.setText("Entrar")
		button_login.clicked.connect(lambda: self.loginApi(txt_correo.text(),passwordtxt.text()))
		button_login.setGeometry(10,90,430,30)
		button_login.setStyleSheet("background-color: #13AA28;")

		button_face = QPushButton(tab)
		button_face.setText("Reconocer face")
		button_face.clicked.connect(lambda: self.faceCapt.reconocimiento(self.LoginShowView))
		button_face.setGeometry(10,130,430,30)
		button_face.setStyleSheet("background-color: #4075CC;")
		
	def loginregister(self, tab):
		labelnombre = QLabel("*Nombre: ", tab)
		labelnombre.setGeometry(10,10,50,25)

		self.nombretxt = QLineEdit(tab)
		self.nombretxt.setGeometry(80,10,350,25)

		labelcorreo = QLabel("*Correo: ", tab)
		labelcorreo.setGeometry(10,40,60,25)

		self.correotxt = QLineEdit(tab)
		self.correotxt.setGeometry(80,40,350,25)

		labelpassword = QLabel("*Password: ", tab)
		labelpassword.setGeometry(10,70,60,25)

		self.passwordtxt =QLineEdit(tab)
		self.passwordtxt.setGeometry(80,70,350,25)
		#self.passwordtxt.setEchoMode(QLineEdit.Password)

		labelconfirmpassword = QLabel("*Confirmar password: ", tab)
		labelconfirmpassword.setGeometry(10,100,110,25)

		self.confirmpasswordtxt = QLineEdit(tab)
		self.confirmpasswordtxt.setGeometry(130,100,300,25)
		#self.confirmpasswordtxt.setEchoMode(QLineEdit.Password)

		btnguardar = QPushButton(tab)
		btnguardar.setText("Guardar")
		btnguardar.setGeometry(10,130,420,30)
		btnguardar.clicked.connect(lambda: self.store([self.nombretxt.text(),self.correotxt.text(),self.passwordtxt.text(),self.confirmpasswordtxt.text()]))
		btnguardar.setStyleSheet("background-color: #13AA28;")

	def check_password(self):
		
		self.session = self.LC.checkLoginC(self.txt_token.text())
		return self.session;

	def loginApi(self,correo,password):
		correo2 = slugify(correo, separator=" ", regex_pattern = r'[^-a-z0-9_@.]+')
		correo3 = correo2.replace(" ", "")
		if "@" in correo3:
			urlapi = config.APIREQUESTLOGIN
			args = {"email":correo3, "password":password}
			response = requests.post(urlapi,params=args)
			data = response.json() 
			if(response.status_code == 200):
				data = response.json() 
				role=self.LC.checkLoginC(data['data']['id'])

				if(len(role)==1):
					self.LoginShowView.close()
					self.principal = Principal.Principal([data['data']['name'],role[0]],self.LoginShowView)
					self.principal.show()
				elif(len(role) > 1):
					self.selectrole(role,data['data']['name'])
				else:
					self.error.messageError("No existe", "No se encontro el usuario 1")
			elif(response.status_code == 401):
				self.error.messageError("Credenciales Incorrectas", "El correo o la contraseña son icorrectas")
		else:
			self.error.messageError("Correo Incorrecto", "El correo ingresado no es valido, ejemplo(correo@example.com)")

	def selectrole(self,roles,nombresession):
		value, ok = QInputDialog.getItem(self, "Roles", "Seleccione el tipo de usuario:", roles)
		if(ok):
			self.LoginShowView.close()
			if(value == 'Administrador'):
				self.principal = Principal.Principal([nombresession,value],self.LoginShowView)
				self.principal.show()
			elif(value == 'Ayudante'):
				self.principal = Principal.Principal([nombresession,value],self.LoginShowView)
				self.principal.show()
		else:
			self.error.messageError("Error 201","Rol no disponible");
			self.LoginShowView.show()

	def store(self, data):
		user = self.LC.store(data)
		if(user):
			self.clearInput()

	def clearInput(self):
		self.nombretxt.clear()
		self.correotxt.clear()
		self.passwordtxt.clear()
		self.confirmpasswordtxt.clear()
