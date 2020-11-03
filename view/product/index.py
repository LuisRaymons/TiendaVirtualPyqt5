from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt as tr
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from random import randint
from config import Variable_entorno as rutePath
from controller import ProductController
import cv2
import os


class Index:
	def __init__(self):
		self.ctrProduct = ProductController.ProductController()
		self.categorias = self.ctrProduct.getCategorias()

		#self.setStyleSheet(open('css/producto.css').read())
		stream = QtCore.QFile("css/producto.css")
		stream.open(QtCore.QIODevice.ReadOnly)
		qApp.setStyleSheet(QtCore.QTextStream(stream).readAll())

	def index(self):
		return self.ctrProduct.consultarColumnas()

	def table(self, data, tabla):
		self.tablRefresh = tabla
		self.tablRefresh.removeRow(len(data)+1)
		#print(data)
		
		for i,(id,nombre,descripcion,costo,precioPorKilo,caducidad,img,id_categoria,created_at,updated_at,deleted_at) in enumerate(data):
			self.tablRefresh.setItem(i, 0, QTableWidgetItem(str(id)))
			self.tablRefresh.setItem(i, 1, QTableWidgetItem(nombre))
			self.tablRefresh.setItem(i, 2, QTableWidgetItem(descripcion))
			self.tablRefresh.setItem(i, 3, QTableWidgetItem(str(costo)))
			self.tablRefresh.setItem(i, 4, QTableWidgetItem(precioPorKilo))
			self.tablRefresh.setItem(i, 5, QTableWidgetItem(str(caducidad)))
			self.tablRefresh.setItem(i, 6, QTableWidgetItem(QIcon(QPixmap(img)),"",0))
			self.tablRefresh.setItem(i, 7, QTableWidgetItem(str(id_categoria)))
			self.tablRefresh.setItem(i, 8, QTableWidgetItem(str(created_at)))
			self.tablRefresh.setItem(i, 9, QTableWidgetItem(str(updated_at)))
			self.tablRefresh.setItem(i, 10, QTableWidgetItem(str(deleted_at)))


		tamanio = len(data) - 1
		
		if(tamanio == -1):
			self.nexIidProduct = 1;
		else:
			self.nexIidProduct = data[tamanio][0] + 1;

	def create(self,tab):
		self.rutaimg = "";
		labelnombre = QLabel("*Nombre: ", tab)
		labelnombre.setGeometry(50,40,100,30)

		nombretxt = QLineEdit(tab)
		nombretxt.setGeometry(145,40,400,30)

		labeldescription = QLabel("*Descripcion: ", tab)
		labeldescription.setGeometry(50,90,100,30)

		descriptiontxt = QPlainTextEdit(tab)
		descriptiontxt.setGeometry(145,90,400,100)

		labelcosto = QLabel("*Costo: ",tab)
		labelcosto.setGeometry(50,140,100,150)

		costotxt = QDoubleSpinBox(tab)
		costotxt.setRange(0.0,999999.99)
		costotxt.setGeometry(145,200,400,30)

		labelpreciokilo = QLabel("Precio por kilo: ", tab)
		labelpreciokilo.setGeometry(50,180,100,150)

		preciokilotxt = QCheckBox(tab)
		preciokilotxt.setGeometry(145,240,400,30)

		labelcaducidad = QLabel("Caducidad: " ,tab)
		labelcaducidad.setGeometry(50,220,100,150)

		self.caducidadtxt = QLineEdit(tab)
		self.caducidadtxt.setGeometry(145,280,400,30)
		
		btncalendar = QPushButton(tab)
		btncalendar.setGeometry(550,280,50,30)
		btncalendar.setIcon(QIcon('icon/calendar.png'))
		btncalendar.clicked.connect(self.calendariofunt)

		labelimg = QLabel("Seleccione imagen: ", tab)
		labelimg.setGeometry(50,270,100,150)

		btnSelectImg = QPushButton(tab)
		btnSelectImg.setText("Seleccione archivo")
		btnSelectImg.setGeometry(145,328,100,30)
		btnSelectImg.clicked.connect(self.fielselect)

		self.img = QLabel(tab)
		self.img.setGeometry(360,328,200,90)

		labelCategoria = QLabel("*Categoria: ", tab)
		labelCategoria.setGeometry(50,360,100,150)

		categoriatxt = QComboBox(tab)
		categoriatxt.setGeometry(145,415,400,30)
		categoriatxt.addItem("Seleccione una colonia")
		categoriatxt.addItems(self.categorias[2])

		btnguardar = QPushButton(tab)
		btnguardar.setText("Guardar")
		btnguardar.setGeometry(50,490,500,30)
		btnguardar.clicked.connect(lambda: self.store([nombretxt.text(),descriptiontxt.toPlainText(),costotxt.text(),preciokilotxt.isChecked(),self.caducidadtxt.text(),self.rutaimg,categoriatxt.currentText()]))

	def calendariofunt(self):
		self.calendarFrame = QDialog()
		self.calendarFrame.setWindowTitle("Calendario")
		self.calendarFrame.setFixedSize(320, 200)
		calendar = QCalendarWidget(self.calendarFrame)
		calendar.setGridVisible(True)
		calendar.move(0, 5)
		calendar.clicked[QDate].connect(self.getDate)
		self.calendarFrame.exec()

	def getDate(self,date):
		self.caducidadtxt.setText(date.toString('yyyy-MM-dd'))
		self.caducidadtxt.setDisabled(True)
		self.calendarFrame.close()

	def fielselect(self):
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
			if not os.path.exists(rutePath.IPRESOURCEIMG +'/productos/'): #  rutePath.IPRESOURCEIMG IPRESOURCEIMG
				os.makedirs(rutePath.IPRESOURCEIMG +'/productos/')
			cv2.imwrite(rutePath.IPRESOURCEIMG +'/productos/' + str(self.nexIidProduct) +'.jpg', imagen)
			self.rutaimg = str(rutePath.IPRESOURCEIMG +'/productos/') + str(self.nexIidProduct)


			saveImgProduct = QPixmap(filename)
			imgProduct = saveImgProduct.scaled(64,64)
			self.img.setPixmap(imgProduct)

	def store(self,data):
		product=self.ctrProduct.store(data)
		if(product == True):
			products = self.ctrProduct.consultarColumnas()
			self.table(products[4],self.tablRefresh)

	def update(self,data):
		categoria = self.ctrProduct.getCategoriaById(data[7])

	
		self.frameupdate = QDialog()
		self.frameupdate.setWindowTitle("Modificando Producto")
		self.frameupdate.setGeometry(QtCore.QRect(320, 110, 700, 550))
		self.frameupdate.setWindowIcon(QIcon('icon/tienda.png'))

		labelnombreupdate = QLabel("*Nombre: ", self.frameupdate)
		labelnombreupdate.setGeometry(50,40,100,30)

		nombreupdatetxt = QLineEdit(self.frameupdate)
		nombreupdatetxt.setGeometry(145,40,400,30)
		nombreupdatetxt.setText(data[1])

		labeldescriptionupdate = QLabel("*Descripcion: ", self.frameupdate)
		labeldescriptionupdate.setGeometry(50,90,100,30)

		descriptionupdatetxt = QPlainTextEdit(self.frameupdate)
		descriptionupdatetxt.setGeometry(145,90,400,100)
		descriptionupdatetxt.setPlainText(data[2])

		labelcostoupdate = QLabel("*Costo: ",self.frameupdate)
		labelcostoupdate.setGeometry(50,140,100,150)

		costoupdatetxt = QDoubleSpinBox(self.frameupdate)
		costoupdatetxt.setRange(0.0,999999.99)
		costoupdatetxt.setGeometry(145,200,400,30)
		#costoupdatetxt.textFromValue(float(data[3]))
		costoupdatetxt.setValue(float(data[3]))
		

		labelpreciokiloupdate = QLabel("Precio por kilo: ", self.frameupdate)
		labelpreciokiloupdate.setGeometry(50,180,100,150)

		preciokiloupdatetxt = QCheckBox(self.frameupdate)
		preciokiloupdatetxt.setGeometry(145,240,400,30)

		if(data[4] == 'true'):
			preciokiloupdatetxt.setCheckState(True)

		labelcaducidadupdate = QLabel("Caducidad: " ,self.frameupdate)
		labelcaducidadupdate.setGeometry(50,220,100,150)

		self.caducidadupdatetxt = QLineEdit(self.frameupdate)
		self.caducidadupdatetxt.setGeometry(145,280,400,30)
		self.caducidadupdatetxt.setText(data[5])
		
		btncalendar = QPushButton(self.frameupdate)
		btncalendar.setGeometry(550,280,50,30)
		btncalendar.setIcon(QIcon('icon/calendar.png'))
		btncalendar.clicked.connect(self.calendariofunt)

		labelimgupdate = QLabel("Seleccione imagen: ", self.frameupdate)
		labelimgupdate.setGeometry(50,270,100,150)

		btnSelectImg = QPushButton(self.frameupdate)
		btnSelectImg.setText("Seleccione archivo")
		btnSelectImg.setGeometry(145,328,100,30)
		btnSelectImg.clicked.connect(self.fielselect)

		saveImgProductupdate = QPixmap(data[6])
		
		#imgProductupdate = saveImgProductupdate.scaled(64,64)
		#print(imgProductupdate)
		

		img = QLabel(self.frameupdate)
		img.setPixmap(saveImgProductupdate)
		img.setGeometry(360,328,200,90)
		

		labelCategoriaupdate = QLabel("*Categoria: ", self.frameupdate)
		labelCategoriaupdate.setGeometry(50,320,100,150)

		labelCategoriaexist = QLabel(categoria[2][1],self.frameupdate)
		labelCategoriaexist.setGeometry(115,375,100,30)
		#print(categoria[2][1])

		categoriaupdatetxt = QComboBox(self.frameupdate)
		categoriaupdatetxt.setGeometry(200,375,320,30)
		categoriaupdatetxt.addItem("Seleccione una colonia")
		categoriaupdatetxt.addItems(self.categorias[2])

		btnguardarupdate = QPushButton(self.frameupdate)
		btnguardarupdate.setText("Guardar")
		btnguardarupdate.setGeometry(50,490,500,30)
		#btnguardarupdate.clicked.connect(lambda: self.store([nombreupdatetxt.text(),descriptionupdatetxt.toPlainText(),costoupdatetxt.text(),preciokiloupdatetxt.isChecked(),self.caducidadupdatetxt.text(),self.rutaimg,categoriaupdatetxt.currentText()]))



		self.frameupdate.exec_()
