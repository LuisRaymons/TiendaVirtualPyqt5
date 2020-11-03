from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import * 
from controller import PromotorController

class Index:
	def __init__(self):
		self.ctrPromotor = PromotorController.PromotorController()

	def index(self):
		return self.ctrPromotor.consultarColumnas()

	def table(self,data,tabla):
		for i,(id,nombre,direccion,telefono,sitioWeb,created_at,updated_at,deleted_at) in enumerate(data):
			tabla.setItem(i, 0, QTableWidgetItem(str(id)))
			tabla.setItem(i, 1, QTableWidgetItem(nombre))
			tabla.setItem(i, 2, QTableWidgetItem(direccion))
			tabla.setItem(i, 3, QTableWidgetItem(telefono))
			tabla.setItem(i, 4, QTableWidgetItem(sitioWeb))
			tabla.setItem(i, 5, QTableWidgetItem(str(created_at)))
			tabla.setItem(i, 6, QTableWidgetItem(str(updated_at)))
			tabla.setItem(i, 7, QTableWidgetItem(str(deleted_at)))

	def create(self, tab):
		nombrelabel = QLabel("*Nombre: ",tab)
		nombrelabel.setGeometry(40,10,60,30)

		nombretxt = QLineEdit(tab)
		nombretxt.setGeometry(100,10,500,30)

		direccionlabel = QLabel("*Direccion: ",tab)
		direccionlabel.setGeometry(40,55,60,30)

		direcciontxt = QLineEdit(tab)
		direcciontxt.setGeometry(100,55,500,30)

		telefonolabel = QLabel("*Telefono: ",tab)
		telefonolabel.setGeometry(40,100,60,30)

		telefonotxt = QLineEdit(tab)
		telefonotxt.setGeometry(100,100,500,30)

		sitiowebLabel = QLabel("Sitio Web:", tab)
		sitiowebLabel.setGeometry(40,145,60,30)

		sitiowebtxt = QLineEdit(tab)
		sitiowebtxt.setGeometry(100,145,500,30)

		btnguardar = QPushButton(tab)
		btnguardar.setText("Guardar")
		btnguardar.setGeometry(40,190,560,30)
		btnguardar.clicked.connect(lambda: self.store([nombretxt.text(),direcciontxt.text(),telefonotxt.text(),sitiowebtxt.text()]))

	def store(self,data):
		self.ctrPromotor.store(data)
