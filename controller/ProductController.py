from modelo import ProductModel
from view.Errors import ErrorGeneral
from datetime import datetime
class ProductController:
    def __init__(self):
        self.mp = ProductModel.ProductModel()
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
    def getCategorias(self):
        try:
            categ = self.mp.getCategorias()
            if(categ[0] == "success" and categ[1] == 200):
                self.categorias = list()
                for cate in categ[2]:
                    self.categorias.append(cate[1])
                valor = ("success", 200,self.categorias)
        except Exception as e:
            valor = ("error", 500, e)
        return valor
    def getProduct(self):
        try:
            product = self.mp.getProduct()
            
            if(product[0] == "success" and product[1] == 200):
                self.productos = list()
                for prod in product[2]:
                    self.productos.append(prod[1])
                valor = ("success", 200,self.productos)
        except Exception as e:
             valor = ("error", 500,"Error en el server")

        return valor
    def store(self,data):
        try:
             datetime.strptime(data[4], '%Y-%m-%d')
        except ValueError:
            self.msm.messageError("Fecha incorrecta", "Presiona el boton del calendario para seleccionar una fecha correcta")
        try:
            if(data[0] != '' and data[1] != '' and data[2] != '' and data[3] != '' and data[6] != 'Seleccione una colonia'):
                confirm = self.msm.messageConfirm("Guardar producto", "¿Realmente desea guardar el producto?")
                if(confirm == True):
                    product = self.mp.store(data)

                    if(product[0] == 'success' and product[1]==200):
                        self.msm.messageInfo("Producto insertado", "El producto fue guardado con exito")
                        return True
                    elif(product[0] == 'warning' and product[1]==400):
                        self.msm.messageInfo("Producto no insertado", product[2])
                        return False
                    elif(product[0] == 'error' and product[1]==500):
                        self.msm.messageInfo("Producto no insertado", "El servidor se encuentra suspendido")
                        return False

            else:
                self.msm.messageError("Campos requeridos", "Los campos marcados por un (*) deven ser llenados")
        except Exception as e:
            raise e

    
    def getCategoriaById(self,id):
        categoria = self.mp.getCategoriaById(id)
        
        if(categoria[0] == "success" and categoria[1] == 200):
            return categoria
        elif(categoria[0] == "error" and categoria[1] == 500):
            self.msm.messageError("Error 500", "Error en el servidor")