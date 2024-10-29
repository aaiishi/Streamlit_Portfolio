import cv2
from cvzone.FaceDetectionModule import FaceDetector
import streamlit as st

# Set up the title and checkbox
st.title("Face Detector")
run = st.checkbox("Run")

# Create an image placeholder
frame_window = st.image([])

# Initialize the FaceDetector
detector = FaceDetector()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Run the face detection when the checkbox is checked
if run:
    while True:
        ret, img = cap.read()
        if not ret:
            st.error("Failed to capture image.")
            break
        
        # Convert the image to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Find faces
        faces, New_Image = detector.findFaces(imgRGB)

        # Display the image in the Streamlit app
        frame_window.image(imgRGB)

# Release the video capture when done
cap.release()
