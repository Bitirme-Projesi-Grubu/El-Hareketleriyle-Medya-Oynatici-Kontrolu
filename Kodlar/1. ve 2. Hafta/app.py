import cv2
import mediapipe
handsModule = mediapipe.solutions.hands

img = cv2.imread(r'C:\Users\ERKAN\Desktop\sol.jpg')
yukseklik, genislik, channels = img.shape

indexler = [handsModule.HandLandmark.INDEX_FINGER_TIP,
           handsModule.HandLandmark.MIDDLE_FINGER_TIP,
           handsModule.HandLandmark.RING_FINGER_TIP,
           handsModule.HandLandmark.PINKY_TIP,
           handsModule.HandLandmark.THUMB_TIP]

yedek = img.copy()
with handsModule.Hands(static_image_mode=True, min_detection_confidence=0.7, max_num_hands=2) as hands:
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for parmak in indexler:
                tip = handLandmarks.landmark[parmak]
                tip_coor =((int)(tip.x*genislik),(int)(tip.y*yukseklik))

                cv2.circle(yedek, tip_coor, 5, (0,0,255), -1)


    cv2.imwrite(r'C:\Users\ERKAN\Desktop\sol_sonuc.jpg', yedek)
    cv2.destroyAllWindows()
    
