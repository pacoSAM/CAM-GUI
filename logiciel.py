# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logiciel.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(630, 471)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("symbole pacosam.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.videoPlayer = phonon.Phonon.VideoPlayer(self.centralwidget)
        self.videoPlayer.setObjectName(_fromUtf8("videoPlayer"))
        self.gridLayout.addWidget(self.videoPlayer, 2, 3, 2, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_cam1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_cam1.setObjectName(_fromUtf8("pushButton_cam1"))
        self.verticalLayout.addWidget(self.pushButton_cam1)
        self.ROT_cam1 = QtGui.QDial(self.centralwidget)
        self.ROT_cam1.setMaximum(179)
        self.ROT_cam1.setObjectName(_fromUtf8("ROT_cam1"))
        self.verticalLayout.addWidget(self.ROT_cam1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout.addWidget(self.label_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButton_cam2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_cam2.setObjectName(_fromUtf8("pushButton_cam2"))
        self.verticalLayout_2.addWidget(self.pushButton_cam2)
        self.ROT_cam2 = QtGui.QDial(self.centralwidget)
        self.ROT_cam2.setMaximum(179)
        self.ROT_cam2.setObjectName(_fromUtf8("ROT_cam2"))
        self.verticalLayout_2.addWidget(self.ROT_cam2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 3, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 3, 2)
        self.verticalSlider = QtGui.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.gridLayout.addWidget(self.verticalSlider, 0, 2, 2, 1)
        self.pushButton_start = QtGui.QPushButton(self.centralwidget)
        self.pushButton_start.setToolTip(u"Aide: Il faut combiner ce bouton avec une autre option")
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.gridLayout.addWidget(self.pushButton_start, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CamControle", None))
        self.comboBox.setItemText(0, _translate("MainWindow", ".......", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Save photo", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "Autorisation Web", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "Save video", None))
        self.comboBox.setItemText(4, _translate("MainWindow", "Impote photo", None))
        self.pushButton_cam1.setText(_translate("MainWindow", "CAM1", None))
        self.label_7.setText(_translate("MainWindow", "Moteur 1", None))
        self.pushButton_cam2.setText(_translate("MainWindow", "CAM2", None))
        self.label.setText(_translate("MainWindow", "Moteur_2", None))
        self.pushButton_start.setText(_translate("MainWindow", "START", None))

from PyQt4 import phonon

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

