from modelo import LoginModelo as mdlLogin
from view.Errors import ErrorGeneral
from slugify import slugify
from config import Variable_entorno as config
import requests
import json

class LoginController:
	def __init__(self):
		self.model=mdlLogin.LoginModelo()
		self.error = ErrorGeneral.ErrorGeneral()

	def checkLoginC(self,id):
		usuario  = self.model.getUser(id)
		role = list()

		if (usuario[0] == 'success' and usuario[1] == 200):
			for u in usuario[2]:
				role.append(u[12])

		return role

	def getUserFace(self, nombre):
		try:
			user = self.model.getUserFace(nombre)
		except Exception as e:
			raise e

	def store(self, data):
		if(data[0] != '' and data[1] != '' and data[3] != ''):
			if(len(data[3])  < 8 and len(data[3]) < 8 ):
				self.error.messageInfo("Contraseña muy corta","Tu contraseña debe tener minimo 8 caracteres")
			else:
				correo2 = slugify(data[1], separator=" ", regex_pattern = r'[^-a-z0-9_@.]+')
				correo3 = correo2.replace(" ", "")
				if "@" in correo3:
					if(data[2] == data[3]):
						urlapi = config.APIREQUESTREGISTER
						args = {"name":data[0],"email":data[1],"password":data[2]}
						response = requests.post(urlapi,params=args)
						data = response.json()
						if(data['message'] == 'Registro sucess'):
							self.error.messageInfo("Registro guardado","Usuario guardado con exitoso")
							return True
						elif(data['message'] == 'Registro existente'):
							self.error.messageInfo("Registro existente","Usuario ya existe en la base de datos")
							return False
						elif(data['message'] == 'Error en el server'):
							self.error.messageInfo("Error 500","Servidor temporalmente apagado")
							return False
					else:
						self.error.messageInfo("las contraseñas no coinciden", "Las contraseñas no son iguales")
						return False
				else:
					self.error.messageError("Correo Incorrecto", "El correo ingresado no es valido, ejemplo(correo@example.com)")
					return False
		else:
			self.error.messageInfo("Campos Requeridos", "Todo los campos marcados por un (*) son requeridos")
			return False