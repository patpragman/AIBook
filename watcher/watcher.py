import cv2
import os
import PIL
import numpy as np

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model_path = os.path.join(os.getcwd(), f'data/haarcascades/haarcascade_eye.xml')
print(haar_model_path)

detectors = [(cv2.CascadeClassifier(os.path.join(os.getcwd(), f'data/haarcascades/{file}')), file) for file in os.listdir("data/haarcascades")]

detector = cv2.CascadeClassifier(haar_model_path)
webcam = cv2.VideoCapture(0)


while True:

    ret, frame = webcam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for detector, name in detectors:

        for feature in detector.detectMultiScale(gray):
            x, y, w, h = feature
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


    # now that we've boxed the frame, go ahead and show it
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
