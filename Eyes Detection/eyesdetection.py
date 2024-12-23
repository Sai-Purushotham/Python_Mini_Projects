import cv2

# Open the camera (use 0 for default camera)
capture = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not capture.isOpened():
    print("Sorry, could not access the camera.")
    exit()  # Exit the program if camera is not accessible

# Load the pre-trained Haar Cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while capture.isOpened():
    # Capture frame-by-frame
    ret, color_image = capture.read()

    # If the frame was not captured correctly, break the loop
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert the captured frame to grayscale
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the grayscale image
    eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    # Count the number of eyes detected
    a = str(len(eyes))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(color_image, a + " eyes detected", (15, 350), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Draw rectangles around the detected eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame with detected eyes
    cv2.imshow('Eye Detection', color_image)

    # Save the frame with detection as an image
    cv2.imwrite('detect.png', color_image)

    # Wait for 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
capture.release()
cv2.destroyAllWindows()
