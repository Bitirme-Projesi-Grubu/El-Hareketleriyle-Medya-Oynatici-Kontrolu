from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QIcon, QColor
from PyQt5 import QtCore, QtWidgets

class Interface(object):
    def setup(self, MainWindow):
        MainWindow.setWindowIcon(QIcon("./icons/app.ico"))
        MainWindow.setFixedSize(750, 500)

        self.mainWidget = QtWidgets.QWidget(MainWindow)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.mainWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 430, 751, 48))

        self.controlCenter = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.controlCenter.setContentsMargins(10, 10, 10, 10)
        self.controlCenter.setSpacing(10)

        self.playButton = QtWidgets.QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(QIcon("./icons/play.ico"))

        self.timeSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setRange(0,0)
        self.timeSlider.setFixedWidth(500)

        self.volumeButton = QtWidgets.QPushButton()
        self.volumeButton.setIcon(QIcon("./icons/volumeOn.ico"))

        self.volumeSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)

        self.controlCenter.addWidget(self.playButton)
        self.controlCenter.addWidget(self.timeSlider)
        self.controlCenter.addWidget(self.volumeButton)
        self.controlCenter.addWidget(self.volumeSlider)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget(self.mainWidget)
        self.videoWidget.setGeometry(QtCore.QRect(0, 0, 751, 431))

        palette = self.videoWidget.palette()
        palette.setColor(self.videoWidget.backgroundRole(), QColor(27,27,27))
        self.videoWidget.setPalette(palette)

        MainWindow.setCentralWidget(self.mainWidget)

        #MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 26))

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuSettings = QtWidgets.QMenu(self.menubar)

        MainWindow.setMenuBar(self.menubar)

        self.actionOpen = QtWidgets.QAction(QIcon("./icons/folder.ico"), "Aç", MainWindow)
        self.actionHandControl = QtWidgets.QAction(MainWindow)
        self.actionHandControl.setCheckable(True)
        self.actionHelp = QtWidgets.QAction(QIcon("./icons/help.ico"), "Aç", MainWindow)

        self.menuFile.addAction(self.actionOpen)
        self.menuSettings.addAction(self.actionHandControl)
        self.menuSettings.addAction(self.actionHelp)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUI(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUI(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Media Player"))
        self.menuFile.setTitle(_translate("MainWindow", "Dosya"))
        self.menuSettings.setTitle(_translate("MainWindow", "Ayarlar"))
        self.actionOpen.setText(_translate("MainWindow", "Aç"))
        self.actionHandControl.setText(_translate("MainWindow", "El İle Kontrol Et"))
        self.actionHelp.setText(_translate("MainWindow", "Yardım"))