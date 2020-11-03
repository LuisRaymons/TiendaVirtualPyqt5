from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import * 
from controller import CateProducController 
from PyQt5.QtGui import QIcon
class Index:
	def __init__(self):
		self.ctrCate = CateProducController.CateProducController()
		
	def index(self):
		return self.ctrCate.consultarColumnas()

	def table(self,data,tabla):
		self.tableRefresh = tabla
		self.dataRefresh = data;
		for i,(id,nombre,created_at,updated_at,deleted_at) in enumerate(self.dataRefresh):
			self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(id)))
			self.tableRefresh.setItem(i, 1, QTableWidgetItem(nombre))
			self.tableRefresh.setItem(i, 2, QTableWidgetItem(str(created_at)))
			self.tableRefresh.setItem(i, 3, QTableWidgetItem(str(updated_at)))
			self.tableRefresh.setItem(i, 4, QTableWidgetItem(str(deleted_at)))

	def create(self,tab):
		labelnombre = QLabel("Nombre: ", tab)
		labelnombre.setGeometry(30,30,100,30)

		self.nombretxt = QLineEdit(tab)
		self.nombretxt.setGeometry(80,30,400,30)

		btnGuardar = QPushButton("Guardar",tab)
		btnGuardar.setGeometry(30,80,450,30)
		btnGuardar.clicked.connect(lambda: self.store(self.nombretxt.text()))

	def store(self,nombre):
		success=self.ctrCate.store(nombre)
		if(success == True):
			self.nombretxt.clear()
			self.table(self.dataRefresh,self.tableRefresh)

	def update(self,data):
		self.frameupdate = QDialog()
		self.frameupdate.setWindowTitle("Modificando Categoria de Producto")
		self.frameupdate.setGeometry(QtCore.QRect(320, 180, 700, 250))
		self.frameupdate.setWindowIcon(QIcon('icon/tienda.png'))

		labelid = QLabel("id",self.frameupdate)
		labelid.setGeometry(20,5,100,30)

		labelidtxt = QLineEdit(self.frameupdate)
		labelidtxt.setGeometry(100,5,500,30)
		labelidtxt.setText(data[0])
		labelidtxt.setDisabled(True)

		labelnombreedit = QLabel("Nombre: ", self.frameupdate)
		labelnombreedit.setGeometry(20,45,100,30)

		txtnombre = QLineEdit(self.frameupdate)
		txtnombre.setGeometry(100,45,500,30)
		txtnombre.setText(data[1])

		btnguardar = QPushButton(self.frameupdate)
		btnguardar.setText("Guardar")
		btnguardar.setGeometry(20,95,580,30)
		btnguardar.clicked.connect(lambda: self.modifcategoria([data[0],txtnombre.text()]))

		self.frameupdate.exec_()

	def modifcategoria(self,data):
		categoria = self.ctrCate.update(data)
		if(categoria == True):
			self.table(self.dataRefresh,self.tableRefresh)
			self.frameupdate.close()

	def destroy(self,data):
		datarefresh = self.index()
		categoria = self.ctrCate.destroy(data)
		self.table(datarefresh[4],self.tableRefresh)

