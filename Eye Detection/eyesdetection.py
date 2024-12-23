import cv2


capture = cv2.VideoCapture(0)


if not capture.isOpened():
    print("Sorry, could not access the camera.")
    exit()  


eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while capture.isOpened():
    
    ret, color_image = capture.read()


    if not ret:
        print("Failed to grab frame.")
        break

    
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

  
    eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    
    a = str(len(eyes))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(color_image, a + " eyes detected", (15, 350), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    
    for (x, y, w, h) in eyes:
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    
    cv2.imshow('Eye Detection', color_image)

    
    cv2.imwrite('detect.png', color_image)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()