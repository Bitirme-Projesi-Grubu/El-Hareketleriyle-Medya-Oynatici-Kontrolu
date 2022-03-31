import cv2, HandModule

capture = cv2.VideoCapture(0)

camWidth, camHeight = 640, 480

capture.set(3, camWidth)
capture.set(4, camHeight)

detector = HandModule.HandDetector(detectionCon=0.65, maxHands=1)


while True:
    success, img = capture.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
      fingers = detector.fingersUp()

      if(fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):
        cv2.putText(img, "SES AYARI", (10, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)
        length, img, array = detector.findDistance(lmList[4],lmList[8], img)
          

    cv2.imshow("Webcam", img)

    if cv2.waitKey(5) & 0xFF == 27:
      break


capture.release()
  
