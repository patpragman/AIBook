import cv2
import os
import tensorflow as tf
import PIL
import numpy as np

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')

detector = cv2.CascadeClassifier(haar_model)
webcam = cv2.VideoCapture(0)

model = tf.keras.models.load_model("smile_model")

while True:

    ret, frame = webcam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for face in detector.detectMultiScale(gray):
        x, y, w, h = face

        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        face_to_examine = frame[y:y + h, x:x + h]

        face_to_examine = cv2.resize(face_to_examine, (64, 64), interpolation=cv2.INTER_AREA)
        im_pil = PIL.Image.fromarray(face_to_examine)
        im_pil = im_pil.resize((64, 64))
        arr = np.asarray(face_to_examine).reshape((1, 64, 64, 3))

        results = model.predict(arr, verbose=0)
        not_smile, smile = results[0]
        if smile <= not_smile:
            print(results)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # now that we've boxed the frame, go ahead and show it
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
webcam.release()
# Destroy all the windows
cv2.destroyAllWindows()
