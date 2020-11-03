from modelo import PromotorModel
from view.Errors import ErrorGeneral
class PromotorController:
    def __init__(self):
        self.mp = PromotorModel.PromotorModel()
        self.msm = ErrorGeneral.ErrorGeneral()
    def consultarColumnas(self):
        try:
            columnas = self.mp.consultarColumnas()
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

    def store(self,data):
        try:
            confirm=self.msm.messageConfirm("Guardar Promotor", "¿Deseas guardar al promotor?")
            if(confirm):
                if(data[0] != '' and data[1] != '' and data[2] != ''):
                    promotor=self.mp.store(data)
                    if(promotor[0] == "success" and promotor[1] == 200):
                        self.msm.messageInfo("Registro guardado", "Su registro de promotor fue guardado con exito")
                    elif(promotor[0] == "warning" and promotor[1] == 300):
                        self.msm.messageError("Error al guardar promotor",promotor[2])
                    elif(promotor[0] == "error" and promotor[1] == 500):
                        self.msm.messageError("Error en el servidor",promotor[2])
                else:
                    self.msm.messageError("Campos requeridos", "Los campos marcados por un (*) son requeridos")                    
        except Exception as e:
            self.msm.messageError("Error 500", "Error en el servidor contacte al administrador")