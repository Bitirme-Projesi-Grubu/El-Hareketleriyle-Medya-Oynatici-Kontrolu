from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        #Pencere'nin genel özellikleri
        self.setWindowTitle("Media Player")
        self.setWindowIcon(QIcon("./icons/app.ico"))
        self.setFixedSize(750, 500)

        #Arkaplan rengi ayarlamak için
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.black)
        self.setPalette(palette)


        self.createPlayer()


    def createPlayer(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        
        self.openButton = QPushButton("OPEN")
        self.openButton.clicked.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(QIcon("./icons/play.ico"))
        self.playButton.clicked.connect(self.playMedia)
        self.playButton.clicked.connect(self.mediaStateChanged)

        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setRange(0,0)
        self.timeSlider.sliderMoved.connect(self.movedMedia)

        self.volumeButton = QPushButton()
        self.volumeButton.setIcon(QIcon("./icons/volumeOn.ico"))
        self.volumeButton.clicked.connect(self.mutedState)

        self.volumeSlider = QSlider(Qt.Horizontal)
        

        horizontalBox = QHBoxLayout()
        horizontalBox.setContentsMargins(0,0,0,0)
        horizontalBox.addWidget(self.openButton)
        horizontalBox.addWidget(self.playButton)
        horizontalBox.addWidget(self.timeSlider)
        horizontalBox.addWidget(self.volumeButton)
        horizontalBox.addWidget(self.volumeSlider)
        
        videoWidget = QVideoWidget()

        verticalBox = QVBoxLayout()
        verticalBox.addWidget(videoWidget)
        verticalBox.addLayout(horizontalBox)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStateChanged)

        #self.mediaPlayer.volumeChanged.connect(self.volumeChanged)

        self.setLayout(verticalBox)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Media")

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    
    def playMedia(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(QIcon("./icons/pause.ico"))
        else:
            self.playButton.setIcon(QIcon("./icons/play.ico"))

    def positionChanged(self, position):
        self.timeSlider.setValue(position)

    def durationChanged(self, duration):
        self.timeSlider.setRange(0, duration)

    def movedMedia(self, position):
        self.mediaPlayer.setPosition(position)

    def setMuted(self, mute):
        self.mediaPlayer.setMuted(mute)

    def mutedState(self):
        if self.mediaPlayer.isMuted():
            self.setMuted(False)
        else:
            self.setMuted(True)

    def isMuted(self):
        return  self.mediaPlayer.isMuted()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())