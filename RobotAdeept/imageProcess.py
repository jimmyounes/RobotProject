import cv2
import base64

def CaptureImage():
    # Open the camera and capture a frame
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()

    # Release the camera
    camera.release()

    # Save the image to a file
    cv2.imwrite("image.jpg", frame)


    # Read the image file
    with open("image.jpg", "rb") as f:
        image_data = f.read()

    # Encode the image data as a base64 string
    image_base64 = base64.b64encode(image_data).decode("utf-8")    

    return image_base64
