from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QUrl

from Interface import Interface
import sys, HandService


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.UI = Interface()
        self.UI.setup(self)

        self.UI.playButton.clicked.connect(self.mediaStateChanged)
        self.UI.timeSlider.sliderMoved.connect(self.moveTimeSlider)

        self.UI.volumeButton.clicked.connect(self.mutedState)
        self.UI.volumeSlider.sliderMoved.connect(self.setVolume)

        self.UI.mediaPlayer.setVideoOutput(self.UI.videoWidget)
        self.UI.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.UI.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.UI.mediaPlayer.mediaStatusChanged.connect(self.mediaStateChanged)

        self.UI.actionOpen.triggered.connect(self.openFile)

        self.UI.actionHandControl.triggered.connect(self.activeHandControl)

        #HandControl Variables
        self.handShortcut = QShortcut(QKeySequence('F9'), self)
        self.handShortcut.activated.connect(self.activeHandControl)
        self.handControl = False
        
        self.play = QShortcut(QKeySequence('p'), self)
        self.pause = QShortcut(QKeySequence('s'), self)

        self.play.activated.connect(self.playMedia)
        self.pause.activated.connect(self.pauseMedia)

        self.setHandShortcuts(self.handControl)
        
        self.thread = HandService.HandServiceThread(self)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", filter="Video (*.mkv *.mp4 *.avi)")

        if fileName != '':
            self.UI.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.UI.playButton.setEnabled(True)
            self.mediaStateChanged()
            self.mediaStateChanged()

    def mediaStateChanged(self):
        if self.UI.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.UI.playButton.setIcon(QIcon("./icons/play.ico"))
            self.UI.mediaPlayer.pause()
        else:
            self.UI.playButton.setIcon(QIcon("./icons/pause.ico"))
            self.UI.mediaPlayer.play()

    def positionChanged(self, position):
        self.UI.timeSlider.setValue(position)

    def durationChanged(self, duration):
        self.UI.timeSlider.setRange(0, duration)

    def moveTimeSlider(self, position):
        self.UI.mediaPlayer.setPosition(position)

    def setVolume(self, value):
        self.UI.mediaPlayer.setVolume(value)

    #HandControl Methods
    def activeHandControl(self):
        self.handControl = not self.handControl
        self.setHandShortcuts(self.handControl)
        self.UI.actionHandControl.setChecked(self.handControl)
        
        if self.handControl:
            self.thread.start()
        else:
            self.thread.stop()

    def setHandShortcuts(self, state):
        self.play.setEnabled(state)
        self.pause.setEnabled(state)

    def playMedia(self):
        self.UI.playButton.setIcon(QIcon("./icons/pause.ico"))
        self.UI.mediaPlayer.play()

    def pauseMedia(self):
        self.UI.playButton.setIcon(QIcon("./icons/play.ico"))
        self.UI.mediaPlayer.pause()

    def setMediaVolume(self, vol):
        self.UI.mediaPlayer.setVolume(vol)
        self.UI.volumeSlider.setValue(self.UI.mediaPlayer.volume())

    def setMuteOn(self):
        self.UI.volumeButton.setIcon(QIcon("./icons/volumeOff.ico"))
        self.UI.mediaPlayer.setMuted(True)
        self.UI.volumeSlider.setValue(0)

    def setMuteOff(self):
        self.UI.volumeButton.setIcon(QIcon("./icons/volumeOn.ico"))
        self.UI.mediaPlayer.setMuted(False)
        self.UI.volumeSlider.setValue(100)

    def mutedState(self):
        if self.UI.mediaPlayer.isMuted():
            self.setMuteOff()
        else:
            self.setMuteOn()

    def playForward(self):
        self.positionChanged(self.UI.mediaPlayer.position() + 5000)
        self.moveTimeSlider(self.UI.mediaPlayer.position() + 5000)
        self.UI.mediaPlayer.play()

    def playBackward(self):
        self.positionChanged(self.UI.mediaPlayer.position() - 5000)
        self.moveTimeSlider(self.UI.mediaPlayer.position() - 5000)
        self.UI.mediaPlayer.play()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())