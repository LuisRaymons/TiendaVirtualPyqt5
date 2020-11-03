from modelo import VentaModel
from view.Errors import ErrorGeneral

class VentaController:
	def __init__(self):
		self.mv = VentaModel.VentaModel()
		self.msm = ErrorGeneral.ErrorGeneral()

	def consultarColumnas(self):
		try:
			columnas = self.mv.consultarColumnas()
			self.columnName = list()
			if(columnas[0] == 'success'):

				for c in (columnas[2]):
					self.columnName.append(c[0])
					valor = ("success", 200,self.columnName,columnas[3], columnas[4], columnas[5])
			else:
				valor = ("success", 202,'','','','')
		except Exception as e:
			valor = ("error", 500, '', '', '', e)
		return valor

	def getClient(self):
		try:
			clientes = self.mv.getClient()
			if(clientes[0] == "success" and clientes[1] == 200):
				self.client = list()
				for c in clientes[2]:
					self.client.append(c[1])
				return self.client
			elif(clientes[0] == "error" and clientes[1] == 500):
				self.msm.messageError("Error en el server",clientes[3])

		except Exception as e:
			self.msm.messageError("Error en el server",e)


	def store(self,data):
		try:
			venta = self.mv.store(data)
			if(venta[0] == "success" and venta[1]==200):
				self.msm.messageInfo("Venta registrada","La venta fue realizada con exito")
			elif(venta[0] == "warning" and venta[1]==300):
				self.msm.messageError("Error al guardar la venta",venta[2])
			elif(venta[0] == "error" and venta[1]==500):
				self.msm.messageError("Error en el servidor",venta[2])
		except Exception as e:
			self.msm.messageError("Error en el servidor", "Error server temporalmente apagado")