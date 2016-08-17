#! /usr/bin/python
# -*- coding: utf-8 -*-
#==========================================================
#Titre: Projet surveillance
#
#
#Par: Paco SAMBA
#===========================================================
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os,time,serial
import numpy as np
import cv2,os
import datetime
from logiciel import*
from arduino import*
from Thread_timer import*
from sendmail import*



def createPath(adresse,namepath):
    os.chdir(adresse)
    if not namepath:
        os.mkdir(namepath)

    os.chdir(Actualposition)


Actualposition=os.getcwd()
createPath(Actualposition,"Video_surveillance")
createPath(Actualposition,"Photo_surveillance")

Ui_MainWindow, Klass=uic.loadUiType("logiciel.ui")


class Surveillance( QMainWindow,Ui_MainWindow):

    def __init__(self, conteneur=None):
        if conteneur is None: conteneur =self
        QMainWindow.__init__(self)
        
        self.setupUi(conteneur)
        self.arduino=ARDUINO()        
        self.photopath=Actualposition +str('/')+"Photo_surveillance"
        self.videopath=Actualposition +str('\\')+"Video_surveillance"
        self.Img2Zoom=0
        self.cam1=0
        self.capturing1=False
        self.cam2=1
        self.capturing2=False       
        self.Image_Actif=0
            
        
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        self.vue=self.graphicsView
        self.scene = QtGui.QGraphicsScene()
        self.progressBar.setMaximum(60)                                 # 1 min d'enregistrement
        self.progressBar.setMinimum(0)


        self.verticalSlider.valueChanged.connect(self.ZoomPict)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(10)
        
        self.pushButton_start.clicked.connect(self.MainStart)
        self.pushButton_cam1.clicked.connect(self.CamWindow)
        self.pushButton_cam2.clicked.connect(self.CamWindow)
        self.pushButton_cam1.setCheckable(True)
        self.pushButton_cam2.setCheckable(True)
        self.connect(self.ROT_cam1 , SIGNAL("valueChanged(int)"),self.MotorRot1)
        self.connect(self.ROT_cam2 , SIGNAL("valueChanged(int)"),self.MotorRot2)

        self.menubar.triggered[QAction].connect(self.MenuBartrigger)

        self.tab=self.addToolBar("Surveillance")
        self.Enable_Surveillance= QAction(QIcon("surveillance.jpg"),"Enable",self)
        self.Enable_Surveillance.setCheckable(True)
        self.tab.addAction(self.Enable_Surveillance)
        self.Disabl_Surveillance= QAction(QIcon("home.png"),"Disable",self)
        self.Disabl_Surveillance.setCheckable(True)
        self.tab.addAction(self.Disabl_Surveillance)

        self.tab.actionTriggered[QAction].connect(self.Main_toolbar_Surveillance)
        self.thr=[]
        self.cap=[]

        self.Media_obj=None

    def Main_toolbar_Surveillance(self,select):
        """Toolbar ( Enable/Diisable) la surveillance"""
        self.arduino.flushBuffer()
        if self.Enable_Surveillance.isChecked():
            self.Disabl_Surveillance.setEnabled(False)
            cv2.destroyAllWindows()
            self.TimeCount(10)
            body_scane = cv2.HOGDescriptor()
            body_scane.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
            thr2=TimerDevice(self.OperationCam1,self.cam1,body_scane)
            self.thr.append(thr2)
            thr2.start()

        else:
            self.Disabl_Surveillance.setEnabled(True)
            self.StopSurveillance()

        if self.Disabl_Surveillance.isChecked():
            self.Enable_Surveillance.setEnabled(False)
            self.StopSurveillance()
            
        else:
            self.Enable_Surveillance.setEnabled(True)


    def MenuBartrigger(self,q):
        """Menu bar fonction"""
        choix= q.text()+" is triggered"
        if choix== "Ouvrir is triggered":
            pict=self.GetFile(Actualposition)
            self.VerfiFilSelect(pict)
        elif choix =="Sauvegard is triggered":
            msg,tr=QInputDialog.getItem(self, u"Sauvegarde", u"Choisir ",[u"PHOTO",u"VIDEO"])
            self.Sauvegard(msg)
        elif choix=="close is triggered":
            os.chdir(Actualposition)
            self.VerfiFilSelect("symbole pacosam.png") 
            QMessageBox.information(self,"Arret du Programme","A Bientot")
            if self.thr:
                for i in self.thr:
                    i.stop()
                    self.arduino.flushBuffer()
            self.arduino.Close()
            self.deleteLater()


    def MainStart(self):
        """Surveillance boutton START et COMBO BOX"""
        action=self.comboBox.currentText()
        if action=="Save photo":
            self.VerifSave_Photo(None)
        elif action=="Save video":
            self.VerifSave_Video(None)
        elif action=="Impote photo":
            img=self.GetFile(self.photopath)
            img=str(img)
            self.Img2Zoom=img
            self.ZoomPict()
        elif action=="Autorisation Web":
            print(action)

    def ActivCam(self,cam):
        """Activation de la cam"""
        return cv2.VideoCapture(cam)

    def StopSurveillance(self):
        """Arret de la surveillance"""
        if self.thr:
            for i in self.thr:
                self.arduino.flushBuffer()
                i.stop()
                self.thr=[]
        if self.cap:
            for i in self.cap:
                i.release()        


    def OperationCam1(self,numcam,body_scane):
        """Camera porte: verifie si quelqu'un à frapper à la porte"""
        if self.arduino.InBuffer():
            if self.arduino.ReadX(5)=="porte":
                os.chdir(self.videopath)
                d=time.strftime("%Y-%m-%d_a_%Hh%Mm%S", time.localtime())
                nameVideo="Porte_le_"+ str(d) +".avi"
                cap=cv2.VideoCapture(numcam)
                fourcc =cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(nameVideo,fourcc, 30.0, (640,480))
                start=time.time()
                end=30
                while(time.time()-start)<end:
                    ret, frame = cap.read()
                    if ret==True:
                        frame = cv2.flip(frame,numcam)
                        out.write(frame)
                        
                self.arduino.flushBuffer()
                cap.release()
                cv2.destroyAllWindows()
                out.release()
                SendMail(nameVideo,nameVideo,"porte")
                os.chdir(Actualposition)

        else:
            cap=self.ActivCam(self.cam2)
            self.OperationCam2(cap,body_scane)
                


    def OperationCam2(self,cap,body_scane):
        """Camera surveillance: detecte les formes humaines"""
        ret,img=cap.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        intrus,w=body_scane.detectMultiScale(gray, winStride=(8,8), padding=(32,32), scale=1.05)
        if intrus !=():
            self.arduino.Write(chr(int(3)))
            SendMail(None,None,None)
                

    def TimeCount(self,t):
        """Count down pour le demmarage de la surveillance"""
        lcdNumber= QtGui.QLCDNumber(self.centralwidget)
        lcdNumber.setGeometry(QtCore.QRect(20, 30, 136, 40))
        lcdNumber.show()
        for i in range(t,-1,-1):
            lcdNumber.display(i)
            time.sleep(1)
            QtGui.qApp.processEvents()                  #continually process events for one second

        lcdNumber.deleteLater()
      

    def Sauvegard(self,message):
        """Conditiion de sauvegarde"""
        if message=="PHOTO":
            getname=QFileDialog.getSaveFileName(self,u"enregistrer sous"," ","PNG(*.png);;JPEG(*.jpg)")
            self.VerifSave_Photo(str(getname))
        elif message=="VIDEO":
            getname=QFileDialog.getSaveFileName(self,u"enregistrer sous"," ","avi(*.avi)")
            self.VerifSave_Video(str(getname))

    
    def VerfiFilSelect(self,namefile):
        """Condition de lecture du fichier"""
        listFormat_video=[".avi",".mpg"]
        listFormat_photo=[".png",".jpg"]
        namefile=str(namefile)
        if namefile[-4:] in listFormat_photo:
            self.Img2Zoom=namefile                            
            self.ZoomPict()                     # On appel la fonction ZoomPict
        elif namefile[-4:] in listFormat_video:
            self.PlayVideo(namefile)

    def PlayVideo(self,namefile):
        """Lecture video"""
        media=phonon.Phonon.MediaSource(namefile)
        obj=self.videoPlayer.mediaObject()
        audioVideo=self.videoPlayer.audioOutput()
        obj.setCurrentSource(media)
        self.Media_obj=obj

        #Video slider
        #=============
        self.seekSlider = phonon.Phonon.SeekSlider(obj,self.centralwidget)
        self.seekSlider.setObjectName("seekSlider")
        self.gridLayout.addWidget(self.seekSlider,  4, 3, 1, 1)

        #Volume slider
        #=============
        
        self.volumeSlider = phonon.Phonon.VolumeSlider(audioVideo,self.centralwidget)
        self.volumeSlider.setObjectName("volumeSlider")
        self.gridLayout.addWidget(self.volumeSlider, 6, 3, 1, 1)

        #Finish video buttton
        #=====================
        self.pushButton_EndVideo = QtGui.QPushButton("EndVideo",self.centralwidget)
        self.pushButton_EndVideo.setObjectName("EndVideo")
        self.gridLayout.addWidget(self.pushButton_EndVideo, 4.3, 2, 1, 1)
        self.pushButton_EndVideo.clicked.connect(self.CloseVideo)          
        obj.play()

    def CloseVideo(self):
        """Fermeture video """
        self.Media_obj.stop()


    def VerifSave_Photo(self,namephoto):
        """Verifie les conditions de sauvegarde photo"""
        if self.pushButton_cam1.isChecked():
            self.SavePicture("cam1",self.Image_Actif,namephoto)
        elif self.pushButton_cam2.isChecked():
            self.SavePicture("cam1",self.Image_Actif,namephoto)
        elif self.pushButton_cam2.isChecked()==self.pushButton_cam1.isChecked():
            QMessageBox.critical(self,"ERREUR","Veuillez choisir une seul et unique Camera")

    def VerifSave_Video(self,namevideo):
        """Verifie les conditions de sauvegarde video"""
        t=60                                # temps d'enregistrement =60
        if self.pushButton_cam1.isChecked():
            self.capturing1=False
            cv2.destroyWindow("cam1")
            self.RecordVideo(self.ActivCam(self.cam1),self.cam1,namevideo,t)
        elif self.pushButton_cam2.isChecked():
            self.capturing2=False
            cv2.destroyWindow("cam2")
            self.RecordVideo(self.ActivCam(self.cam2),self.cam2,namevideo,t)
        elif self.pushButton_cam2.isChecked()==self.pushButton_cam1.isChecked():
            QMessageBox.critical(self,"ERREUR","Veuillez choisir une seul et unique Camera")


    def MotorRot1(self):
        """Rotation Servo-Moteur"""
        moteur1=1
        angleCam1=self.ROT_cam1.value()
        self.PiloteMotor(moteur1,angleCam1)

    def MotorRot2(self):
        """Rotation Servo-Moteur"""
        moteur2=2
        angleCam2=self.ROT_cam2.value()
        self.PiloteMotor(moteur2,angleCam2)


    def PiloteMotor(self,NumMotor,angle):
        """Envoie de l'angle selectionné au Servo-Moteur"""
        self.arduino.Write(chr(int(NumMotor)))
        self.arduino.Write(chr(int(angle)))

    def CamWindow(self):
        """Gere la fenetre d'affichage"""
        if self.pushButton_cam1.isChecked():
            self.pushButton_cam2.setEnabled(False)
            self.capturing1=True
            cap1=self.ActivCam(self.cam1)
            while self.capturing1==True:
                k=self.FindFace(cap1,1)
                if k==27:
                    break

        elif self.pushButton_cam1.isChecked()==False:
            self.pushButton_cam2.setEnabled(True)
            self.capturing1=False
            cv2.destroyWindow("cam1") 
            
        if self.pushButton_cam2.isChecked():
            self.pushButton_cam1.setEnabled(False)
            self.capturing2=True
            cap2=self.ActivCam(self.cam2)
            while self.capturing2==True:
                k=self.FindFace(cap2,2)
                if k==27:
                    break
            
        elif self.pushButton_cam2.isChecked()==False:
            self.pushButton_cam1.setEnabled(True)
            self.capturing2=False
            cv2.destroyWindow("cam2") 

    def ZoomPict(self):
        """Zoom image selectionné"""
        val=self.verticalSlider.value()
        if self.Img2Zoom!=0:   
            image=cv2.imread(self.Img2Zoom)
            h, w = image.shape[:2]
            height=h*(1+0.1*val)
            width=w*(1+0.1*val)
            frame = QtGui.QImage(image.data, w, h, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(frame).scaled(width, height, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation)
            
            self.scene.addPixmap(pixmap)
            self.graphicsView.setScene(self.scene)
            self.graphicsView.show()
            

    
    def FindFace(self,cap,name):
        """Détecte le visage"""
        name=str('cam')+str(name)
        ret,img=cap.read()
        self.Image_Actif=img
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=self.face_cascade.detectMultiScale(gray,1.3,5)
        if faces!=():
            self.SavePicture(name,img,None)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes=self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow(name,img)
        k=cv2.waitKey(35) & 0xff
        return k

    def SavePicture(self,namecam,img,namephoto):
        """Capture de l'image  en format png"""
        if not namephoto:
            d=time.strftime("%Y-%m-%d %Hh%Mm%S", time.localtime())
            namephoto=namecam +str(d)+".png"
        else:
            namephoto=namephoto
        os.chdir(self.photopath)
        cv2.imwrite(namephoto,img)
        os.chdir(Actualposition)


    def RecordVideo(self,Activcam,numcam,namevideo,endRecord):
        """Enregistre la video en .avi"""
        # pensez à installer xvid codec
        if not namevideo:
            name=QInputDialog.getText(self, self.trUtf8("Nom de la Video"),self.trUtf8("Entrez Le nom de la video"),QLineEdit.Normal)
            VideoName=str(name[0])+".avi"
        else:
            VideoName=namevideo
            
        cap = Activcam

        fourcc =cv2.VideoWriter_fourcc(*'XVID')
        os.chdir(self.videopath)
        out = cv2.VideoWriter(str(VideoName),fourcc, 20.0, (640,480))
        start=time.time()
        
        while(time.time()-start)<endRecord:
            ret, frame = cap.read()
            val=time.time()-start
            self.progressBar.setValue(val)
            if ret==True:
                frame = cv2.flip(frame,numcam)
                out.write(frame)
                cv2.imshow(VideoName,frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    QMessageBox.critical(self,"Erreur","Attendre la fin de l'enregistrement")
                
            else:
                break
        cv2.destroyWindow(VideoName)
        if not namevideo:
            QMessageBox.information(self,"Enregistrement","<b>Enregistrement termine</b>")
            
        self.progressBar.setValue(0)
        os.chdir(Actualposition)
        

    def GetFile(self,path):
        """Getfile from path"""
        os.chdir(path)
        pict=QFileDialog.getOpenFileName(self)
        os.chdir(Actualposition)
        return pict


    
if __name__=="__main__":

    a=QApplication(sys.argv)
    #try:
    f=Surveillance()
    f.show()
    a.exec_()
    

    #except:
        #print"Erreur possible:\n"
        #print"1-Arduino non Connecte","\n","2-Le programme est deja ouvert"
        #pass

