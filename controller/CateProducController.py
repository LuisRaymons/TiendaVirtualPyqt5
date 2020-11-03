from modelo import CateProducModel
from view.Errors import ErrorGeneral

class CateProducController:
	def __init__(self):
		self.mcp=CateProducModel.CateProducModel()
		self.msm=ErrorGeneral.ErrorGeneral()
		
	def consultarColumnas(self):
		try:
			columnas = self.mcp.consultarColumnas()
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
	def store(self,nombre):
		if(nombre != ''):
			result = self.mcp.store(nombre)

			if(result[0] == 'succes' and result[1] == 200):
				self.msm.messageInfo("Categoria guardada", "El registro de la categoria de producto se guardo con exito")
				return True
			elif(result[0] == 'warning' and result[1] == 300):
				self.msm.messageError("Error al ingresar nombre", result[2])
				return False
			elif(result[0] == 'warning' and result[1] == 202):
				self.msm.messageError("Error categoria ya existente", result[2])
				return False

			elif(result[0] == 'eror' and result[1] == 500):
				self.msm.messageError("Nombre requerido", result[2])
				return False
		else:
			self.msm.messageError("Nombre requerido", "El nombre es requerido")
			return False
	def update(self,data):
		
		try:
			categoria = self.mcp.update(data)
			if(categoria[0] == "success" and categoria[1] == 200):
				self.msm.messageInfo("Categoria guardado","El registro de categoria de producto guardado con exito")
				return True
			elif(categoria[0] == "warning" and categoria[1] == 300):
				self.msm.messageError("Error al guardar categoria", categoria[2])
				return False
			elif(categoria[0] == "error" and categoria[1] == 500):
				self.msm.messageError("Error en el servidor",categoria[2])	
				return False			
		except Exception as e:
			self.msm.messageError("Error en el servidor",e)
			return False
	def destroy(self,data):
		try:
			confirm = self.msm.messageConfirm("Eliminar Categoria de Producto", "¿Realmente desea eliminar a la categoria de producto?")
			
			if(confirm):
				categoria = self.mcp.destroy(data)
				print(categoria)
				if(categoria[0] == "success" and categoria[1] == 200):
					self.msm.messageInfo("Eliminado","La categoria fue eliminado con exito")
					return True
				elif(categoria[0] == "warning" and categoria[1] == 300):
					self.msm.messageError("Error al eliminar categoria de producto",categoria[2])
				elif(categoria[0] == "error" and categoria[1] == 500):
					self.msm.messageError("Error en el servidor","Ocurrio un error en el servidor al intentar eliminar la categoria de producto")
					return False
		except Exception as e:
			self.msm.messageError("Error en el servidor","Ocurrio un error en el servidor al intentar eliminar la categoria de producto")
			return False
					
