from config import Variable_entorno as rutePath
from view.Errors import ErrorGeneral as msg
from view import Principal,LoginView
from controller import LoginController
import cv2 
import os
import imutils
import numpy as np
from PIL import Image

class CapturaRostro:
	def __init__(self):
		super(CapturaRostro, self).__init__()
		self.mensaje=msg.ErrorGeneral()
		self.loginc = LoginController.LoginController()
		
	def capturaFace(self,nombre):
		self.nombre = nombre
		self.loginc.getUserFace(nombre)

		msConfi  = self.mensaje.messageConfirm("Preparando reconocimiento", "¿ Estas preparado para tu reconocimiento facial, comensara en 30 segundos(Asegurate de no tener lentes) ?")

		if(msConfi == True):
			if nombre == 0:
				return			
			personName = nombre
			dataPath = rutePath.IPRESOURCEIMG + "/facesDetecter" #Cambia a la ruta donde hayas almacenado Data
			personPath = dataPath + '/' + personName
			if not os.path.exists(personPath):
			    print('Carpeta creada: ',personPath)
			    os.makedirs(personPath)
			cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
			faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
			count = 0
			while True:
			    
			    ret, frame = cap.read()
			    if ret == False: break
			    frame =  imutils.resize(frame, width=640)
			    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			    auxFrame = frame.copy()
			    faces = faceClassif.detectMultiScale(gray,1.3,5)
			    for (x,y,w,h) in faces:
			        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
			        rostro = auxFrame[y:y+h,x:x+w]
			        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
			        cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
			        count = count + 1
			    cv2.imshow('frame',frame)
			    k =  cv2.waitKey(1)
			    if k == 27 or count >= 100:
			        break
			cap.release()
			cv2.destroyAllWindows()
			#self.entrenamiento() 
			return True

	def entrenamiento(self):
		self.mensaje.messageInfo("Entrenando rostros.....","El entrenamiento de rostros puede tardar varios minutos, tenga pasiencia")
		dataPath = rutePath.IPRESOURCEIMG + "/facesDetecter"
		modelPath = dataPath + "/modelPath"
		if not os.path.exists(modelPath):
			os.makedirs(modelPath)
		peopleList = os.listdir(dataPath)
		labels = []
		facesData = []
		label = 0
		for nameDir in peopleList:
		    personPath = dataPath + '/' + nameDir
		    for fileName in os.listdir(personPath):
		        labels.append(label)
		        facesData.append(cv2.imread(personPath+'/'+fileName,cv2.IMREAD_GRAYSCALE))
		    label = label + 1
		face_recognizer = cv2.face.EigenFaceRecognizer_create()
		face_recognizer.train(facesData, np.array(labels))
		face_recognizer.write(modelPath + '/modeloLBPHFace.xml')
		self.mensaje.messageInfo("Almacenando rostros","Los rostros fueron entrenados con exito")
		
	def reconocimiento(self,ventanaLogin):
		self.ventanalogin = ventanaLogin
		dataPath = rutePath.IPRESOURCEIMG + "/facesDetecter"
		modelPath = dataPath + "/modelPath"
		imagePaths = os.listdir(dataPath)
		face_recognizer = cv2.face.EigenFaceRecognizer_create()
		#Verificar que exista el archivo xml si no existe mandarle un mensaje de que se registre primero
		
		if os.path.exists(modelPath + '/modeloLBPHFace.xml'):
			face_recognizer.read(modelPath + '/modeloLBPHFace.xml')
			cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
			faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
			while True:
				ret,frame = cap.read()
				if ret == False: break
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				auxFrame = gray.copy()
				faces = faceClassif.detectMultiScale(gray,1.3,5)
				for (x,y,w,h) in faces:
					rostro = auxFrame[y:y+h,x:x+w]
					rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
					result = face_recognizer.predict(rostro)
					cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

					if result[1] < 5700:
						cap.release()
						cv2.destroyAllWindows()
						self.login = LoginView.LoginView()
						self.principal = Principal.Principal(['Usuario detectado por rostro'],ventanaLogin)
						ventanaLogin.close()
						self.principal.show()
					else:
						cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
					if result[1] < 500:
						cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
					else:
						cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
					if result[1] < 70:
						cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
					else:
						cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)


				cv2.imshow('frame',frame)
				k = cv2.waitKey(1)
				if k == 27:
					break
			cap.release()
			cv2.destroyAllWindows()
		else:
			self.mensaje.messageInfo("Modelo de facess no existe", "El modelo de face no existe llame a su administrador")
			

