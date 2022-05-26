import cv2, HandModule
import numpy as np
from PyQt5.QtCore import QThread
from PyQt5.QtMultimedia import QMediaPlayer

class HandServiceThread(QThread):
    def __init__(self, mediaPlayer):
        super().__init__()
        self._run_flag = True
        self.player = mediaPlayer

    def run(self):
        self._run_flag = True
        self.tempVolume = 0
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camWidth, camHeight = 640, 480

        capture.set(3, camWidth)
        capture.set(4, camHeight)

        self.detector = HandModule.HandDetector(detectionCon=0.65, maxHands=1)

        while self._run_flag:
            success, img = capture.read()
            img = cv2.flip(img, 1)
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                value = self.detector.createData(img)
                predict = self.detector.predictHand(value)

                if predict == "durdur":
                    self.player.pauseMedia()
                elif predict == "oynat":
                    self.player.playMedia()
                elif predict == "sustur":
                    self.player.setMuteOn()
                elif predict == "sesAc":
                    self.player.setMuteOff()
                elif predict == "ileriSar":
                    self.player.playForward()
                elif predict == "geriSar":
                    self.player.playBackward()

            cv2.waitKey(225)

        capture.release()

    def stop(self):
        self._run_flag = False
        self.wait()

            

            