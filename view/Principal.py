from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt as tr
from PyQt5.QtGui import QIcon,QFont
from os import remove, path
import sys
import math
from view.almacen import index as almacenview
from view.cliente import index as clienteview
from view.cproduct import index as catProductView
from view.product import index as productview
from view.usuario import index as usuarioview
from view.promotor import index as promotorview
from view.venta import index as ventaview
from moduloFace import CapturaRostro

from view.Errors import ErrorGeneral as msmview


class Principal(QtWidgets.QMainWindow):
	def __init__(self, data, loginview):
		self.data = data
		self.loginview = loginview		
		self.nameSession = data[0] 
		self.role = data[1]


		# cargar la pagina principal
		super(Principal, self).__init__()
		self.setWindowTitle('Ventana Principal')
		self.setWindowIcon(QIcon('icon/tienda.png'))
		self.setFont(QFont("Times", 50, QFont.Bold))
		self.setGeometry(0,0,1350,650)




		self.widget = QtWidgets.QWidget(self)
		self.widget.setGeometry(QtCore.QRect(0, 0, 191, 690))
		self.widget.setObjectName("widget")

		# inicar la vista de errores
		self.error = msmview.ErrorGeneral()
		# crear todas las vistas
		self.viewalmacen = almacenview.Index()
		self.viewcliente = clienteview.Index()
		self.viewcproduct = catProductView.Index()
		self.viewproduct = productview.Index()
		self.viewusuario = usuarioview.Index()
		self.viewpromotor = promotorview.Index()
		self.viewventa = ventaview.Index()
		
		#Creacion del arvol de menus
		self.treeView = QtWidgets.QTreeWidget(self.widget)
		self.treeView.setGeometry(QtCore.QRect(0, 0, 210, 690))
		self.treeView.setObjectName("treeView")

		item_1 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_2 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_3 = QtWidgets.QTreeWidgetItem(self.treeView)
		recursotreview = QtWidgets.QTreeWidgetItem(self.treeView)
		cateproducttreview = QtWidgets.QTreeWidgetItem(recursotreview)
		producttreview = QtWidgets.QTreeWidgetItem(recursotreview)
		clienttreview = QtWidgets.QTreeWidgetItem(recursotreview)
		promotoretreview = QtWidgets.QTreeWidgetItem(recursotreview)
		almacentreview = QtWidgets.QTreeWidgetItem(recursotreview)
		usertreview = QtWidgets.QTreeWidgetItem(recursotreview)
		ventatreview = QtWidgets.QTreeWidgetItem(recursotreview)
		item_12 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_13 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_14 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_15 = QtWidgets.QTreeWidgetItem(self.treeView)
		item_16 = QtWidgets.QTreeWidgetItem(self.treeView)

		#sa.setIcon(0,QIcon('icon/treeviewIcon/recurso.ico'))

		recursotreview.setIcon(0,QIcon('icon/treeviewIcon/recurso.ico'))
		cateproducttreview.setIcon(0,QIcon('icon/treeviewIcon/cateproduct.ico'))
		producttreview.setIcon(0,QIcon('icon/treeviewIcon/product.ico'))
		clienttreview.setIcon(0,QIcon('icon/treeviewIcon/client.ico'))
		promotoretreview.setIcon(0,QIcon('icon/treeviewIcon/promotore.ico'))
		almacentreview.setIcon(0,QIcon('icon/treeviewIcon/almacen.ico'))
		usertreview.setIcon(0,QIcon('icon/treeviewIcon/user.ico'))
		ventatreview.setIcon(0,QIcon('icon/treeviewIcon/venta.ico'))
		item_14.setIcon(0,QIcon('icon/treeviewIcon/cerrarsession.ico'))
		

		_translate = QtCore.QCoreApplication.translate
		self.widget.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.treeView.headerItem().setText(0, _translate("MainWindow", "StartBootsrap"))
		__sortingEnabled = self.treeView.isSortingEnabled()
		self.treeView.setSortingEnabled(False)

		self.treeView.topLevelItem(0).setText(0, _translate("MainWindow", "CORE"))
		self.treeView.topLevelItem(1).setText(0, _translate("MainWindow", "DashBoard"))
		self.treeView.topLevelItem(2).setText(0, _translate("MainWindow", "INTERFACE"))
		self.treeView.topLevelItem(3).setText(0, _translate("MainWindow", "Recursos"))
		self.treeView.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "Categoria Producto"))
		self.treeView.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "Producto"))
		self.treeView.topLevelItem(3).child(2).setText(0, _translate("MainWindow", "Cliente"))
		self.treeView.topLevelItem(3).child(3).setText(0, _translate("MainWindow", "Promotor"))
		self.treeView.topLevelItem(3).child(4).setText(0, _translate("MainWindow", "Almacen"))
		self.treeView.topLevelItem(3).child(5).setText(0, _translate("MainWindow", "Users"))
		self.treeView.topLevelItem(3).child(6).setText(0, _translate("MainWindow", "Ventas"))
		self.treeView.topLevelItem(4).setText(0, _translate("MainWindow", "ADDONS"))
		self.treeView.topLevelItem(5).setText(0, _translate("MainWindow", "Charts"))
		self.treeView.topLevelItem(6).setText(0, _translate("MainWindow", "Tables"))
		self.treeView.topLevelItem(6).setText(0, _translate("MainWindow", "Entrar reconocimiento facial"))
		self.treeView.topLevelItem(6).setText(0, _translate("MainWindow", "Cerrar Session"))
		self.treeView.setSortingEnabled(__sortingEnabled)
		self.treeView.clicked.connect(self.getValue)
		self.setStyleSheet(open('css/principal.css').read())
	# a que vista sera mandado cuando de click al arbol
	def getValue(self,ix=""):
		if(ix=="cliente"):
			self.opcionSelect="Cliente"
		else:
			self.opcionSelect = ix.data()

		if (self.opcionSelect == 'Almacen'):
			columns = self.viewalmacen.index()
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Almacen')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Cliente'):
			columns = self.viewcliente.index(1,20)
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Cliente')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Categoria Producto'):
			columns = self.viewcproduct.index()
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Categoria Producto')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Producto'):
			columns =  self.viewproduct.index()
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Producto')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Users'):
			columns = self.viewusuario.index()
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Users')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Promotor'):
			columns = self.viewpromotor.index()
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Promotor')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Ventas'):
			
			columns = self.viewventa.index()
			#print(columns)
			if(columns[0] == 'success' and columns[1] == 200):
				self.TableLoading(columns[2],columns[3], columns[4], columns[5], 'Ventas')
			elif(columns[0] == 'error' and columns[1] == 500):
				print("Obtubimos un error en la bd")
		elif(self.opcionSelect == 'Entrar reconocimiento facial'):
			#Borrar primero el archivo y despues crearlo otra ves
			ruta = "img/src/facesDetecter/modelPath/modeloLBPHFace.xml"
			#remove(ruta)
			if path.exists(ruta):
				remove(ruta)
			self.rostro = CapturaRostro.CapturaRostro()
			self.rostro.entrenamiento()
		elif(self.opcionSelect == 'Cerrar Session'):
			self.close()
			self.loginview.show()


	# Creacion de la tabla dependiendo de que le den click al arbol del menu
	def TableLoading(self,columnName,columnCount,columndata, columndataCount, tipotable):
		self.pagina = math.ceil(columndataCount[0]/20)
		_translate = QtCore.QCoreApplication.translate
		self.frameTable = QtWidgets.QWidget(self)
		self.frameTable.setGeometry(QtCore.QRect(80, 0, 1265, 700))
		self.frameTable.setObjectName("table")

		self.tabWidget = QtWidgets.QTabWidget(self.frameTable)
		self.tabWidget.setGeometry(QtCore.QRect(110, 0, 1265, 700))
		self.tabWidget.setObjectName("tabWidget")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.tabWidget.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		
		self.tabWidget.addTab(self.tab_2, "")
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Datos"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Nuevo"))
		self.tableWidget = QtWidgets.QTableWidget(self.tab)
		self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1150, 635))
		self.tableWidget.setColumnCount(columnCount[0]) # Nombre de las columnas
		self.tableWidget.setRowCount(columndataCount[0])   #  numero de registros insertados
		self.tableWidget.setHorizontalHeaderLabels(columnName)
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #  desa bilitar la edicion
		self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows) # seleccionar toda la fila
		
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.tableWidget.setContextMenuPolicy(tr.CustomContextMenu)
		self.tableWidget.customContextMenuRequested.connect(self.menuContextual)

			
		if(tipotable == 'Almacen'):
			if(self.role in('Administrador','Ayudante')):
				self.viewalmacen.table(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewalmacen.create(self.tab_2,self.data[0])
		elif(tipotable == 'Cliente'):
			if(self.role in('Administrador','Ayudante')):
				self.viewcliente.table(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewcliente.create(self.tab_2)
		elif(tipotable == 'Categoria Producto'):
			if(self.role in('Administrador','Ayudante')):
				self.viewcproduct.table(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewcproduct.create(self.tab_2)	
		elif(tipotable == 'Producto'):
			if(self.role in('Administrador','Ayudante')):
				self.viewproduct.table(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewproduct.create(self.tab_2)		
		elif(tipotable == 'Users'):
			print(self.role)
			if(self.role in('Administrador','Ayudante')):
				self.viewusuario.tabla(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewusuario.create(self.tab_2)		
		elif(tipotable == 'Promotor'):
			if(self.role in('Administrador','Ayudante')):
				self.viewpromotor.table(columndata,self.tableWidget)
			if(self.role in('Administrador')):
				self.viewpromotor.create(self.tab_2)
		elif(tipotable == 'Ventas'):
			if(self.role in('Administrador','Ayudante')):
				self.viewventa.table(columndata,self.tableWidget)
			if(self.role in('Administrador','Ayudante')):
				self.viewventa.create(self.tab_2,self.data[0])			

		self.frameTable.show()

	def menuContextual(self, posicion):
		indices = self.tableWidget.selectedIndexes()
		filaSeleccionada = [dato.text() for dato in self.tableWidget.selectedItems()]
		
		if indices:
			menu = QMenu()
			if(self.role in('Administrador')):
				updateMenu = menu.addAction(QIcon('icon/actualizar.ico'),"Modificar", lambda: self.modificateFunction(filaSeleccionada))
				
			if(self.role in('Administrador')):
				destroyMenu = menu.addAction(QIcon('icon/destroy.ico'),"Eliminar", lambda: self.deleteFunction(filaSeleccionada))
			if(self.role in('Administrador') and self.opcionSelect == 'Users'):
				detailMenu = menu.addAction(QIcon('icon/detailrole.ico'),"Roles y Permisos", lambda: self.detailfunction(filaSeleccionada,self.role))
				
			menu.addSeparator()
			menu.addSeparator()
			menu.exec_(self.tableWidget.viewport().mapToGlobal(posicion))

	def modificateFunction(self,data):
		if(self.opcionSelect == 'Categoria Producto'):
			self.viewcproduct.update(data)
		elif(self.opcionSelect == 'Producto'):
			self.viewproduct.update(data)
		elif(self.opcionSelect == 'Cliente'):
			self.viewcliente.update(data)
			self.getValue("cliente")
		elif(self.opcionSelect == 'Promotor'):
			print("hola")
		elif(self.opcionSelect == 'Almacen'):
			print("hola")

	def deleteFunction(self, data):
		if(self.opcionSelect == 'Categoria Producto'):
			self.viewcproduct.destroy(data)
		elif(self.opcionSelect == 'Producto'):
			self.ctrProduct.update(data)
		elif(self.opcionSelect == 'Cliente'):
			confirDelete=self.viewcliente.destroyCliente(data)
			if(confirDelete == True):
				self.getValue("cliente")
			elif(confirDelete == False):
				self.error.messageConfirm("Error de usuario", "¡El cliente que inteta eliminar no existe!")
		elif(self.opcionSelect == 'Promotor'):
			print("hola")
		elif(self.opcionSelect == 'Almacen'):
			print("hola")

	def detailfunction(self,data,role):
		if(self.opcionSelect == 'Users'):
			self.viewusuario.detailrole(data,role)


		








