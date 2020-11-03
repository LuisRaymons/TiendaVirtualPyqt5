from modelo import ClienteModel
from view.Errors import ErrorGeneral

class ClienteController:
    def __init__(self):
        self.mc = ClienteModel.ClienteModel()
        self.error = ErrorGeneral.ErrorGeneral()
    def consultarColumnas(self, inicio, fin):
        try:
            columnas = self.mc.consultarColumnas(inicio, fin)
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

    def getColonia(self):
        try:
            colonias = self.mc.getColonia()
            self.colonia = list()
            if(colonias[0] == 'success'):
                for c in (colonias[2]):
                    self.colonia.append(c[1])
                valor = ("success", 200, self.colonia)
            else:
                valor = ("success", 202,'')
        except Exception as e:
             valor = ("success", 500, e)

        return valor

    def saveCliente(self, data):
        confirmMsm=self.error.messageConfirm("Guardar Cliente","¿Desea guardar el cliente?");
        if(confirmMsm==True):
            #Validar que el numero telefonico tenga menos de 10 digitos y verificar si son numeros
            if(data[0] != '' and data[1]!= '' and data[2] != '' and data[3] != '' and  data[4] != ''):
                model=self.mc.store(data)
                print(model)
            else:
                self.error.messageError("Error 202","Debe ingresar todo los datos que tengan una *");

    def consultarColonia(self, idcolonia):
        try:
            colonia = self.mc.consultarColonia(idcolonia)
        except Exception as e:
            raise e
        return colonia

    def update(self, data):
        try:
            clienteUpdate=updateClient = self.mc.update(data)
            valor = ("success",200, clienteUpdate)
        except Exception as e:
            valor = ("error",500, e)
        return valor;

    def destroy(self,id):
        if(type(id) == int):
            clienteDestroy=self.mc.destroy(id)
            valor=("success", 200,clienteDestroy)
            return clienteDestroy;
        else:
            valor=("success", 202,"Cancelado movimiento")
        return valor;
        
