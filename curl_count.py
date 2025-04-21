import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("AiTrainer/Curls.mp4")

detector = pm.poseDetector()
count = 0
count2 = 0
dir = 0
dir2 = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    #img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #right arm
        angle1 = detector.findAngle(img, 12, 14, 16)
        #left arm
        angle = detector.findAngle(img, 11, 13, 15)
        per2 = np.interp(angle1, (60, 170), (100, 0))
        per = np.interp(angle, (60, 170), (100, 0))
        per = np.interp(angle1, (210, 310), (100, 0))
        per3 = np.interp(angle, (210, 310), (100, 0))
       #for right arm (60, 170), (0, 100) is the range of motion
        # print(angle, per)
        #check for curls
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        if per2 == 100:
            if dir2 == 0:
                count2 += 0.5
                dir2 = 1
        if per2 == 0:
            if dir2 == 1:
                count2 += 0.5
                dir2 = 0

        # Draw left arm stats (bên trái màn hình)
        # Progress bar background
        cv2.rectangle(img, (20, 150), (120, 400), (0, 255, 0), 3)
        # Progress bar fill
        bar_height = int(np.interp(per, (0, 100), (400, 150)))
        cv2.rectangle(img, (20, bar_height), (120, 400), (0, 255, 0), cv2.FILLED)
        # Percentage text
        cv2.putText(img, f'left arm', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, f'{int(per)}%', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        # Rep counter
        cv2.putText(img, f'Count: {int(count)}', (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Draw right arm stats (bên phải màn hình)
        # Progress bar background
        cv2.rectangle(img, (1100, 150), (1200, 400), (0, 255, 0), 3)
        # Progress bar fill
        bar_height2 = int(np.interp(per2, (0, 100), (400, 150)))
        cv2.rectangle(img, (1100, bar_height2), (1200, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'right arm', (1090, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        # Percentage text
        cv2.putText(img, f'{int(per2)}%', (1090, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        # Rep counter
        cv2.putText(img, f'Count: {int(count2)}', (1090, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Curl Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()