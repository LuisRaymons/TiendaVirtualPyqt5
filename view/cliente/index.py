from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QIcon
from controller import ClienteController as ctrCliente
from view.Errors import ErrorGeneral as msmview


class Index:
	def __init__(self):
		self.ctrClient = ctrCliente.ClienteController()
		self.colonias = self.ctrClient.getColonia()
		self.error = msmview.ErrorGeneral()
	def index(self,inicio,fin):
		return self.ctrClient.consultarColumnas(inicio,fin)
	def table(self,data,tabla):
		for i,(id,nombre,apellidos,telefono,direccion,id_colonia,created_at,updated_at,deleted_at) in enumerate(data):
			tabla.setItem(i, 0, QTableWidgetItem(str(id)))
			tabla.setItem(i, 1, QTableWidgetItem(nombre))
			tabla.setItem(i, 2, QTableWidgetItem(apellidos))
			tabla.setItem(i, 3, QTableWidgetItem(telefono))
			tabla.setItem(i, 4, QTableWidgetItem(direccion))
			
			tabla.setItem(i, 5, QTableWidgetItem(str(id_colonia)))
			tabla.setItem(i, 6, QTableWidgetItem(str(created_at)))
			tabla.setItem(i, 7, QTableWidgetItem(str(updated_at)))
			tabla.setItem(i, 8, QTableWidgetItem(str(deleted_at)))
	def create(self,tab):
		nombreLabel = QLabel('* Nombre: ',tab)
		nombreLabel.setGeometry(0, 0, 100, 100)
		apellidosLabel = QLabel('* Apellidos: ',tab)
		apellidosLabel.setGeometry(0, 0, 100, 200)
		telefonoLabel = QLabel('* Telefono: ',tab)
		telefonoLabel.setGeometry(0, 0, 100, 300)
		DireccionLabel = QLabel('* Direccion: ',tab)
		DireccionLabel.setGeometry(0, 0, 100, 400)
		ColoniaLabel = QLabel('* Colonia: ',tab)
		ColoniaLabel.setGeometry(0, 0, 100, 500)

		nombreTxt = QLineEdit(tab)
		nombreTxt.setGeometry(60,30,650,30)

		apellidosTxt = QLineEdit(tab)
		apellidosTxt.setGeometry(60,80,650,30)

		telefonoTxt = QLineEdit(tab)
		telefonoTxt.setGeometry(60,130,650,30)

		direccionTxt = QLineEdit(tab)
		direccionTxt.setGeometry(60,180,650,30)

		coloniaTxt = QComboBox(tab)
		coloniaTxt.setGeometry(60,230,650,30)
		coloniaTxt.addItem("Seleccione una colonia")
		coloniaTxt.addItems(self.colonias[2])

		btnGuardar = QPushButton("Guardar",tab)
		btnGuardar.setGeometry(0,280,700,30)
		btnGuardar.clicked.connect(lambda: self.ctrClient.saveCliente([nombreTxt.text(),apellidosTxt.text(),telefonoTxt.text(),direccionTxt.text(),coloniaTxt.currentText()]))
	def update(self,data):
		self.framUpdateCliente = QDialog()
		self.framUpdateCliente.setWindowTitle("Modificando Cliente")
		self.framUpdateCliente.setGeometry(QtCore.QRect(320, 180, 700, 250))
		self.framUpdateCliente.setWindowIcon(QIcon('icon/tienda.png'))
		
		labelNombre = QLabel("Nombre cliente: ",self.framUpdateCliente)
		labelNombre.setGeometry(20,5,100,30)
		
		nombreEdit = QLineEdit(self.framUpdateCliente)
		nombreEdit.setGeometry(100,5, 500,30)
		nombreEdit.setText(data[1])

		labelApellidos = QLabel("Apellidos: ", self.framUpdateCliente)
		labelApellidos.setGeometry(20,40,100,30)

		apellidosEdit = QLineEdit(self.framUpdateCliente)
		apellidosEdit.setGeometry(100,40,500,30)
		apellidosEdit.setText(data[2])

		telefonoLabel = QLabel("Telefono", self.framUpdateCliente)
		telefonoLabel.setGeometry(20,80,100,30)

		telefonoEdit = QLineEdit(self.framUpdateCliente)
		telefonoEdit.setGeometry(100,80,500,30)
		telefonoEdit.setText(data[3])

		direccionLabel = QLabel("Direccion:", self.framUpdateCliente)
		direccionLabel.setGeometry(20,120,100,30)

		direccionEdit = QLineEdit(self.framUpdateCliente)
		direccionEdit.setGeometry(100,120,500,30)
		direccionEdit.setText(data[4])

		coloniaLabel = QLabel("Colonia: ", self.framUpdateCliente)
		coloniaLabel.setGeometry(20,160,100,30)
		#print("La data es: " + data[5])
		colonia=self.ctrClient.consultarColonia(data[5])
		self.coloniaselected = str(colonia[2][1])
		

		self.coloniaSelect = QComboBox(self.framUpdateCliente)
		self.coloniaSelect.setGeometry(200,160,400,30)
		self.coloniaSelect.addItem("Seleccione una colonia")
		self.coloniaSelect.addItems(self.colonias[2])

		labelColoniatxt = QLabel(self.coloniaselected,self.framUpdateCliente)
		labelColoniatxt.setGeometry(100,160,90,30)


		btnGuardar = QPushButton(self.framUpdateCliente)
		btnGuardar.setText("Guardar Cambios")
		btnGuardar.setGeometry(20,200,585,30)
		btnGuardar.pressed.connect(lambda: self.modifClient([data[0],nombreEdit.text(),apellidosEdit.text(),telefonoEdit.text(),
																   direccionEdit.text(),self.coloniaSelect.currentText()]))
		
		self.framUpdateCliente.exec_()
	def modifClient(self,data):
		cliente=self.ctrClient.update(data)
		if(cliente[0] == "success" and cliente[1] == 200):
			self.framUpdateCliente.close()
	def destroyCliente(self, data):
		confirm=self.error.messageConfirm("Eliminando Cliente", "Seguro que quieres eliminar al cliente: " + str(data[1]) + " " + str(data[2]));
		
		if(confirm == True):
			clienteDestroy=self.ctrClient.destroy(int(data[0]))
			if(clienteDestroy[0]=='success' and clienteDestroy[1]==200):
				return True
			elif(clienteDestroy[0]=='success' and clienteDestroy[1]==202):
				return False
				


