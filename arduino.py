#-*- coding: utf-8 -*-
#================================================================"
#Titre: Class RS485
#
#description: Port serie ARDUINO USB avec ces principales attributions
#
#Auteur: Paco SAMBA
#================================================================

#   I-Librairie:
#     ----------
import serial


#   II-Variable
#      ----------

baudRate=115200
nomPort="COM12"
timeOut=0.01
try:
    ser=serial.Serial(nomPort,baudRate,timeout=timeOut)
except:
    print("ARDUINO INDETECTABLE")

# III- Class ARDUINO
#      -------------

class ARDUINO():

    def __init__(self):

        self.port=ser

    def InBuffer(self):
        return self.port.inWaiting()

    def Open(self):
        if  self.Isopen()!=True:
            self.port.open()

    def Close(self):
        self.port.close()

    def Write(self,message):
        self.port.write(message)

    def Read(self):
        """Lit tous le contenus du buffer"""
        return self.port.readline()

    def ReadX(self,nombre_de_bytes):
        """nombre de bytes à lire"""
        x=nombre_de_bytes
        return self.port.read(x)

    def Isopen(self):
        """Retourn True or False selon l'etat du port"""
        return self.port.isOpen()


    def flushBuffer(self):
        """Permet de vider le buffer"""
        self.port.flushInput()
