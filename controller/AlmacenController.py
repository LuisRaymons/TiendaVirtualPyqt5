from modelo import AlmacenModel
class AlmacenController:
    def __init__(self):
        self.ma = AlmacenModel.ALmacenModel()
    def consultarColumnas(self):
        try:
            columnas = self.ma.consultarColumnas()
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

    def store(self,data1,data2):
        try:
            almacen=self.ma.store(data1,data2) 
            return almacen      
        except Exception as e:
            valor=("error", 500, e)
            return valor