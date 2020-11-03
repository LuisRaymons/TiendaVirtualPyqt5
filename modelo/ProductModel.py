from config import Conexion
from datetime import datetime
class ProductModel:
    def __init__(self):
        self.con = Conexion.Conexion()
        self.conectar=self.con.conexion()
    def consultarColumnas(self):
        try:
            sql = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'COLUMNS')"
            self.conectar[3].execute(sql)
            tablaColumnName = self.conectar[3].fetchall()

            sql2 = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'COUNTCOLUMN')"
            self.conectar[3].execute(sql2)
            totalColumns = self.conectar[3].fetchone()

            sql3 = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'READ')" 
            self.conectar[3].execute(sql3)
            products = self.conectar[3].fetchall()

            sql4 = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'COUNTDATA')"
            self.conectar[3].execute(sql4)
            productsCount = self.conectar[3].fetchone()

            valores =("success", 200, tablaColumnName, totalColumns, products,productsCount)
        except Exception as e:
            valores =("error", 500, '' , '', '', '')

        return valores
    def getCategorias(self):
        try:
            sql = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'CATEGORIAS')"
            self.conectar[3].execute(sql)
            categorias = self.conectar[3].fetchall()
            valores = ("success", 200, categorias)
        except Exception as e:
            valores = ("error", 500, e)

        return valores
    def getProduct(self):
        try:
            sql = "CALL sp_producto(0,'','',0.00,'','0000-00-00','',0,'READ')"
            self.conectar[3].execute(sql)
            productos = self.conectar[3].fetchall()

            valores = ("success", 200, productos)
        except Exception as e:
            valores = ("error", 500, e)
        return valores
    def store(self, data):
        try:
            precioKilo = 'true'  if(data[3] == True)  else 'false'
            imgloading = "" if(data[5] == "") else str(data[5] + ".jpg")
            sqlcate= "CALL sp_producto(0,%s,'',0.00,'','0000-00-00','',0,'CATEGORIASEXISTS')"
            valexist = (str(data[6]))
            self.conectar[3].execute(sqlcate,valexist)
            categoria = self.conectar[3].fetchone()
           

            if(categoria[1] != '' and categoria[0] != 0):

                sql = "CALL sp_producto(0,%s,%s,%s,%s,%s,%s,%s,'CREATE')"
                val =(data[0],str(data[1]),str(data[2]),precioKilo,str(data[4]),imgloading,str(categoria[0]))
                
                retornoProduct=self.conectar[3].execute(sql,val)
                self.conectar[2].commit()
                
                if(retornoProduct == 1):
                    valor = ("success", 200,data)
                else:
                    valor = ("warning", 400, "No se pudo insertar el producto")
        except Exception as e:
            valor = ("error", 500, e)
        return valor

    def getCategoriaById(self,idCat):
        try:
            sqlcateI="CALL sp_producto(%s,'','',0.00,'','0000-00-00','',0,'CATEGORIABYID')"
            valIdCate = (str(idCat))
            valIdCateidate = self.conectar[3].execute(sqlcateI,valIdCate)
            categobyid = self.conectar[3].fetchone()
           
            if(valIdCateidate == 1):
                valor = ("success", 200, categobyid)
            else:
                valor = ("warning",300, "Error en el proceso")
        except Exception as e:
            valor = ("error", 500, e)
        return valor

    