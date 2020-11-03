from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from controller import AlmacenController, ProductController
from config import Variable_entorno as rutePath
from view.Errors import ErrorGeneral
import cv2
import os
class Index:
	def __init__(self):
		self.ctrAlmacen = AlmacenController.AlmacenController()
		self.ctrproduct = ProductController.ProductController()
		self.products = self.ctrproduct.getProduct()
		self.msm = ErrorGeneral.ErrorGeneral()

	def index(self):
		return self.ctrAlmacen.consultarColumnas()
	def table(self, data,tabla):
		for i,(id,folio,imgFolio,entrada,salida,stock,id_user,id_producto,created_at,updated_at,deleted_at) in enumerate(data):
			tabla.setItem(i, 0, QTableWidgetItem(str(id)))
			tabla.setItem(i, 1, QTableWidgetItem(folio))

			tabla.setItem(i, 2, QTableWidgetItem(imgFolio))
			tabla.setItem(i, 3, QTableWidgetItem(entrada))
			tabla.setItem(i, 4, QTableWidgetItem(salida))
			tabla.setItem(i, 5, QTableWidgetItem(str(stock)))
			tabla.setItem(i, 6, QTableWidgetItem(str(id_user)))
			tabla.setItem(i, 7, QTableWidgetItem(str(id_producto)))

			tabla.setItem(i, 8, QTableWidgetItem(str(created_at)))
			tabla.setItem(i, 9, QTableWidgetItem(str(updated_at)))
			tabla.setItem(i, 10, QTableWidgetItem(str(deleted_at)))

		self.tamanio = len(data) + 1		

	def create(self,tab,data):

		self.rutaimg = "";
		
		foliolabel = QLabel("*Folio: ", tab)
		foliolabel.setGeometry(40,20,50,30)

		foliotxt = QLineEdit(tab)
		foliotxt.setGeometry(100,20,500,30)

		labelimg = QLabel("Imagen: ", tab)
		labelimg.setGeometry(40,60,50,30)

		btnfile = QPushButton(tab)
		btnfile.setText("Seleccionar archivo")
		btnfile.clicked.connect(self.selectimg)
		btnfile.setGeometry(100,60,500,30)

		self.img = QLabel(tab)
		self.img.setGeometry(700,60,40,30)

		entradaslabel = QLabel("*Entradas: ", tab)
		entradaslabel.setGeometry(40,100,50,30)

		entradastxt = QSpinBox(tab)
		entradastxt.setGeometry(100,100,500,30)

		productlabel = QLabel("*Producto: ", tab)
		productlabel.setGeometry(40,140,50,30)

		producttxt = QComboBox(tab)
		producttxt.setGeometry(100,140,500,30)
		producttxt.addItem("Seleccione un producto entrante")
		producttxt.addItems(self.products[2])

		btnguardar = QPushButton(tab)
		btnguardar.setText("Guardar")
		btnguardar.setGeometry(40,180,560,30)
		btnguardar.clicked.connect(lambda:self.store([foliotxt.text(),entradastxt.text(),self.rutaimg,producttxt.currentText()],data))

	def selectimg(self):
		self.fileFrame = QDialog()
		self.fileFrame.setWindowTitle("Archivo para imagen")
		self.fileFrame.setFixedSize(320, 200)
		self.openFileNameDialog()

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		filename, _ = QFileDialog.getOpenFileName(self.fileFrame,"Seleccione una imagen del producto", "","All Files (*);;PNG,JPG,JPEG Image(*.png,*.jpg,*.jpeg)", options=options)
		if filename:
			imagen = cv2.imread(filename)
			if not os.path.exists(rutePath.IPRESOURCEIMG +'/almacen/'): #  rutePath.IPRESOURCEIMG IPRESOURCEIMG
				os.makedirs(rutePath.IPRESOURCEIMG +'/almacen/')
			cv2.imwrite(rutePath.IPRESOURCEIMG +'/almacen/' + 'almacen_' + str(self.tamanio) +'.jpg', imagen)
			self.rutaimg = str(rutePath.IPRESOURCEIMG +'/almacen/') + str(self.tamanio)

			saveImgalmacen = QPixmap(filename)
			imgalmacen = saveImgalmacen.scaled(64,64)
			self.img.setPixmap(imgalmacen)

	def store(self,data1,data2):
		if(data2 != ''):
			if(data1[0] != '' and data1[1] != '' and data1[3] != 'Seleccione un producto entrante'):
				validate = self.msm.messageConfirm("Guardar Almacen","¿Desea guardar el registro de almacen?")
				if(validate):
					almacen=self.ctrAlmacen.store(data1,data2)
					if(almacen[0] == 'success' and almacen[1]==200):
						self.msm.messageInfo("Almacen guardado","El registro de almacen se guardo con exito")
					elif(almacen[0] == 'warning' and almacen[1]==300):
						self.msm.messageError("Error al guardar almacen",almacen[2])
					elif(almacen[0] == 'error' and almacen[1]==500):
						self.msm.messageError("Error en el servidor",almacen[2])					
			else:
				self.msm.messageInfo("Campos requeridos", "Debes completar los campos que tengan un (*)")
		else:
			self.msm.messageError("Usuario incorrecto", "El usuario que intenta relacionar no existe")
