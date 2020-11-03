from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import * 
from controller import VentaController
from view.Errors import ErrorGeneral

class Index:
	def __init__(self):
		self.ctrVenta = VentaController.VentaController()
		self.msm = ErrorGeneral.ErrorGeneral()
		self.client = self.ctrVenta.getClient()
	def index(self):
		return self.ctrVenta.consultarColumnas()

	def table(self,data,tabla):

		for i,(id,factura,impuesto,precio_total,tipoPago,id_cliente,id_users) in enumerate(data):
			tabla.setItem(i, 0, QTableWidgetItem(str(id)))
			tabla.setItem(i, 1, QTableWidgetItem(factura))
			tabla.setItem(i, 2, QTableWidgetItem(str(impuesto)))
			tabla.setItem(i, 3, QTableWidgetItem(str(precio_total)))
			tabla.setItem(i, 4, QTableWidgetItem(tipoPago))
			tabla.setItem(i, 5, QTableWidgetItem(str(id_cliente)))
			tabla.setItem(i, 6, QTableWidgetItem(str(id_users)))

	def create(self,tab,user):
		facturalabel = QLabel("factura: ", tab)
		facturalabel.setGeometry(10,10,50,30)

		facturatxt = QLineEdit(tab)
		facturatxt.setGeometry(100,10,500,30)

		impustoslabel = QLabel("Impustos: ", tab)
		impustoslabel.setGeometry(10,50,50,30)

		impuestotxt = QDoubleSpinBox(tab)
		impuestotxt.setGeometry(100,50,500,30)

		preciototallabel = QLabel("Precio total: ", tab)
		preciototallabel.setGeometry(10,90,60,30)

		preciototaltxt = QDoubleSpinBox(tab)
		preciototaltxt.setRange(0.0,999999.99)
		preciototaltxt.setGeometry(100,90,500,30)

		tipoPagoLabel = QLabel("tipo de pago: ", tab)
		tipoPagoLabel.setGeometry(10,130,80,30)

		tipopagotxt = QComboBox(tab)
		tipopagotxt.setGeometry(100,130,500,30)
		tipopagotxt.addItem("Seleccione el tipo de pago")
		tipopagotxt.addItems(['Contado','Tarjeta master card','Tarjeta debito','Tarjeta de credito'])

		clientelabel = QLabel("Cliente: ", tab)
		clientelabel.setGeometry(10,170,50,30)

		clientetxt = QComboBox(tab)
		clientetxt.setGeometry(100,170,500,30)
		clientetxt.addItem("Seleccione cliente")
		clientetxt.addItems(self.client)

		btnGuardar = QPushButton(tab)
		btnGuardar.setText("Guardar")
		btnGuardar.setGeometry(10,210,590,30)
		btnGuardar.clicked.connect(lambda: self.store([facturatxt.text(),impuestotxt.text(),preciototaltxt.text(),tipopagotxt.currentText(),clientetxt.currentText(), user]))

	def store(self,data):
		if(data[0] != '' and data[1] != 0.00 and data[2] != 0.00 and data[3] != 'Seleccione el tipo de pago' and data[4] != 'Seleccione cliente' and data[4] != ''):
			confirm = self.msm.messageConfirm("Guardar Venta", "¿Desea guardar la venta?")
			if(confirm):
				self.ctrVenta.store(data)


		else:
			self.msm.messageError("Campos requeridos", "Los campos marcados por un (*) deben ser compleltados")

