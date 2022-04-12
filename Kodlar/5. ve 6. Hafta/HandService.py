import cv2, HandModule
import numpy as np
from PyQt5.QtCore import QThread

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
                self.volumeControl(img)

        capture.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def volumeControl(self, img):
        fingers = self.detector.fingersUp()

        if(fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):
            cv2.putText(img, "SES AYARI", (10, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)
            length, img, array = self.detector.findDistance(self.detector.lmList[4],self.detector.lmList[8], img)
            vol = np.interp(length, [45,220], [0,100])
            self.player.setMediaVolume(vol)

            

            