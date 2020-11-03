from modelo import UserModel
from view.Errors import ErrorGeneral
from moduloFace import CapturaRostro
from slugify import slugify
from config import Variable_entorno as config
import requests
import json


class UserController:
    def __init__(self):
        self.mu = UserModel.UserModel()
        self.error = ErrorGeneral.ErrorGeneral()
        self.captura = CapturaRostro.CapturaRostro()
    def consultarColumnas(self):
        try:
            columnas = self.mu.consultarColumnas()
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

    def getRole(self):
        try:
            roles = self.mu.getRole()
            if(roles[0] == 'success' and roles[1]==200):
                self.role = list()
                for rol in  roles[2]:
                    self.role.append(rol[1])
                valores = ('success',200,self.role)
        except Exception as e:
            valores("error",500,e)
        return valores
    
    def Reconocer(self,nombre):
        if(nombre != ''):
            valorCaptura=self.captura.capturaFace(nombre)
            if(valorCaptura == True):
                self.error.messageInfo("Registro guardado", "Su registro se guardo con exito")
                #self.error.messageToast("Registro guardado", "¡El registro de reconocimiento de guardo con exito!")
            
        else:
            self.error.messageError("Error 202","Debe ingresar el nombre del usuario");

    def store(self, data):
        if(data[0] != '' and data[1] != '' and data[2] != 'Seleccione el Role del usuario' and data[3] != '' and data[4] != ''):
            if(len(data[3])  < 8 and len(data[3]) < 8 ):
                self.error.messageInfo("Contraseña muy corta","Tu contraseña debe tener minimo 8 caracteres")
            else:
                correo2 = slugify(data[1], separator=" ", regex_pattern = r'[^-a-z0-9_@.]+')
                correo3 = correo2.replace(" ", "")
                if "@" in correo3:
                    if(data[3] == data[4]):
                        urlapi = config.APIREQUESTREGISTER
                        args = {"name":data[0],"email":data[1],"password":data[3], "role":data[2]}
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

    def roles(self, iduser):
        if(iduser != '' or iduser != 0):
            roles=self.mu.roles(iduser)
            
           
            roleAll = list()
            if(roles[0] == 'success' and roles[1] == 200):
                if(len(roles) > 0):                    
                    for rol in roles[2]:
                        role  = (rol[2],rol[5])

                        roleAll.append(role)
                        
            return tuple(roleAll)
