import sim
import sys
import time
import cv2
import numpy as np
import math

class Bot:
    def __init__(self, ip="127.0.0.1", port=19999):
        self.sen_Izq = "LeftSensor"
        self.sen_Der = "RightSensor"
        self.sen_Mid = "MiddleSensor"
        self.ip = ip
        self.port = port
        self.activo = True
        self.clientID = -1
        self.connect()
        self.init_elements()

    def connect(self):
        print ('Programa inicio')
        sim.simxFinish(-1) # cerrar todas las conexiones
        # Conectar a CoppeliaSim
        self.clientID=sim.simxStart(self.ip,self.port,True,True,5000,5)
        if(self.clientID == -1):
            print("Imposible conectar")
            self.activo = False

    def init_elements(self):
        if(self.activo == False):
            return
        #Guardar la referencia de la camara
        _, self.camLeft = sim.simxGetObjectHandle(self.clientID, self.sen_Izq, sim.simx_opmode_oneshot_wait)
        _, self.camMid = sim.simxGetObjectHandle(self.clientID,self.sen_Mid, sim.simx_opmode_oneshot_wait)
        _, self.camRight = sim.simxGetObjectHandle(self.clientID, self.sen_Der, sim.simx_opmode_oneshot_wait)

        imgL = self.get_image(self.camLeft)
        imgM = self.get_image(self.camMid)
        imgR = self.get_image(self.camRight)
        time.sleep(1)

    def get_image(self, idcam):
        if(self.activo == False):
            return

        _, resolution, image=sim.simxGetVisionSensorImage(self.clientID, idcam, 0, sim.simx_opmode_streaming)
        if(len(resolution) == 0):
            print("No pudo conectarse a la camara {}".format(idcam))
            return None
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def execute(self):
        if(self.activo == False):
            return

        while(1):
            imgL = self.get_image(self.camLeft)
            imgM = self.get_image(self.camMid)
            imgR = self.get_image(self.camRight)

            #Mostrar frame y salir con "ESC"
            cv2.imshow('Left', imgL)
            cv2.imshow('Right', imgR)
            cv2.imshow('Middle', imgM)

            tecla = cv2.waitKey(5) & 0xFF
            if tecla == 27:
                break
        #cerrar
        sim.simxFinish(self.clientID)

def main():
    ex = Bot()
    ex.execute()

if __name__ == '__main__':
    main()
