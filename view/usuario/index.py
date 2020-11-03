from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
#from PyQt5.QtCore import Qt as tr
from PyQt5.QtWidgets import * 
from controller import UserController
from view.Errors import ErrorGeneral


class Index:
	def __init__(self):
		self.ctrUser = UserController.UserController()
		self.roles = self.ctrUser.getRole()
		self.msm = ErrorGeneral.ErrorGeneral()

	def index(self):
		return self.ctrUser.consultarColumnas()
	def tabla(self,data,table):

		for i,(id,name,email,remember_token,created_at,updated_at) in enumerate(data):
			table.setItem(i, 0, QTableWidgetItem(str(id)))
			table.setItem(i, 1, QTableWidgetItem(name))

			table.setItem(i, 2, QTableWidgetItem(email))
			table.setItem(i, 3, QTableWidgetItem(remember_token))

			table.setItem(i, 4, QTableWidgetItem(str(created_at)))
			table.setItem(i, 5, QTableWidgetItem(str(updated_at)))

	def create(self, tab):
		nombreLabel = QLabel('* Nombre: ',tab)
		nombreLabel.setGeometry(10, 10, 60, 30)
		self.nombreTxt = QLineEdit(tab)
		self.nombreTxt.setGeometry(120,10,650,30)
		
		emailLabel = QLabel('* Correo: ',tab)
		emailLabel.setGeometry(10, 50, 60, 30)
		self.emailTxt = QLineEdit(tab)
		self.emailTxt.setGeometry(120,50,650,30)

		roleLabel = QLabel('* Role: ',tab)
		roleLabel.setGeometry(10, 90, 60, 30)
		self.RoleTxt = QComboBox(tab)
		self.RoleTxt.setGeometry(120,90,650,30)
		self.RoleTxt.addItem("Seleccione el Role del usuario")
		self.RoleTxt.addItems(self.roles[2])

		passwordLabel = QLabel("*Contraseña: ",tab)
		passwordLabel.setGeometry(10,130,70,30)
		self.passwordtxt = QLineEdit(tab)
		self.passwordtxt.setGeometry(120,130,650,30)

		passwordconfirmLabel = QLabel("*Confirma constreña: ", tab)
		passwordconfirmLabel.setGeometry(10,170,110,30)
		self.passwordconfirmtxt = QLineEdit(tab)
		self.passwordconfirmtxt.setGeometry(120,170,650,30)

		btnFaceRecod = QPushButton("Reconocimiento facial", tab)
		btnFaceRecod.setGeometry(10,230,760,30)
		btnFaceRecod.clicked.connect(lambda: self.ctrUser.Reconocer(self.nombreTxt.text()))

		btnGuardar = QPushButton("Guardar",tab)
		btnGuardar.setGeometry(10,280,760,30)
		btnGuardar.clicked.connect(lambda: self.store([self.nombreTxt.text(),self.emailTxt.text(),self.RoleTxt.currentText(),self.passwordtxt.text(),self.passwordconfirmtxt.text()]))

	def store(self,data):
		user =self.ctrUser.store(data)
		if(user):
			self.clearinput()

	def clearinput(self):
		self.nombreTxt.clear()
		self.emailTxt.clear()
		self.passwordtxt.clear()
		self.passwordconfirmtxt.clear()
		self.RoleTxt.clear()
		self.RoleTxt.addItem("Seleccione el Role del usuario")
		self.RoleTxt.addItems(self.roles[2])

	def detailrole(self,data,role):
		self.role = role
		roles = self.ctrUser.roles(data[0])		

		ventanadetail = QDialog()
		ventanadetail.setFixedSize(400,300)
		ventanadetail.setWindowTitle('Agregar o quitar roles y permisos')

		tituloRole = QLabel(ventanadetail)
		tituloRole.setText("Roles del usuario: ")
		tituloRole.setGeometry(10,10,90,30)

		nombreuserlabel = QLabel(ventanadetail)
		nombreuserlabel.setText(data[1])
		nombreuserlabel.setGeometry(100,10,450,30)
		nombreuserlabel.setStyleSheet("color:#1E63E2;")
		
		self.tablatole = QTableWidget(ventanadetail)
		self.tablatole.setGeometry(10,40,320,100)
		self.tablatole.setRowCount(len(roles))  
		self.tablatole.setColumnCount(2) 
		self.tablatole.setAlternatingRowColors(True)
		self.tablatole.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablatole.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tablatole.setHorizontalHeaderLabels(["id","nombre"])
		self.tablatole.horizontalHeader().setStretchLastSection(True)
		self.tablatole.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.tablatole.customContextMenuRequested.connect(self.menuroletable)


		for i,(id,name) in enumerate(roles):
			self.tablatole.setItem(i, 0, QTableWidgetItem(str(id)))
			self.tablatole.setItem(i, 1, QTableWidgetItem(name))

		buttonagregarRole = QPushButton(ventanadetail)
		buttonagregarRole.setText("Agregar nuevo Rol")
		buttonagregarRole.setGeometry(40,200,100,30)


		buttonpermisos = QPushButton(ventanadetail)
		buttonpermisos.setText("Asignar Permiso Especial")
		buttonpermisos.setGeometry(180,200,130,30)
		
			
		#self.role.addItems(roles['namerole'])
		

		ventanadetail.setWindowIcon(QIcon('icon/tienda.png'))


		ventanadetail.exec_()

	def menuroletable(self, posicion):

		indices = self.tablatole.selectedIndexes()
		filaSeleccionada = [dato.text() for dato in self.tablatole.selectedItems()]

		if indices:
			menurole = QMenu()		
			if(self.role in('Administrador')):
				destroyMenu = menurole.addAction(QIcon('icon/destroy.ico'),"Eliminar", lambda: self.deleterole(filaSeleccionada))
	
			menurole.addSeparator()
			menurole.addSeparator()
			menurole.exec_(self.tablatole.viewport().mapToGlobal(posicion))

	def deleterole(self,data):
		print(data)


