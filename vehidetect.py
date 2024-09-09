import cv2
import pygame
import controller as cd

# Initialize pygame mixer
pygame.mixer.init()

vehiclexml = cv2.CascadeClassifier('vehicle.xml')

# Constants for distance estimation
KNOWN_WIDTH = 2.0  # Width of the car in meters
FOCAL_LENGTH = 1000.0  # Focal length of the camera in pixels (example value)

def detection(frame):
    vehicle = vehiclexml.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in vehicle:
        # Ensure the detected object is of reasonable size
        if w > 30 and h > 30:
            # Increase rectangle size by multiplying width and height by a factor
            x -= int(w * 0.1)  # Decrease x-coordinate
            y -= int(h * 0.1)  # Decrease y-coordinate
            w += int(w * 0.2)  # Increase width
            h += int(h * 0.2)  # Increase height
           
            # Draw rectangle around the detected vehicle
            cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
           
            # Estimate distance to the car
            distance = estimate_distance(w)

            if distance < 50:            
                # Play sound when vehicle is detected
                pygame.mixer.music.load('beep-warning-6387.mp3')  # Replace 'beep-warning-6387.mp3' with the path to your sound file
                pygame.mixer.music.play()
                print("A CAR IS PRESENT WITHIN DISTANCE",distance)
                cd.vib(1)
            else:
                print(distance)
                cd.vib(0)
           
            # Display distance information
            cv2.putText(frame, f'vehicle detected, distance: {distance:.2f} meters', (x+w, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
    return frame

def estimate_distance(object_width):
    # Estimate distance using simple geometry (assuming known width and focal length)
    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / object_width
    return distance

def capturescreen():
    realtimevideo = cv2.VideoCapture(0)
    while realtimevideo.isOpened():
        ret, frame = realtimevideo.read()
        controlkey = cv2.waitKey(1)
        if ret:
            # Resize the frame to double its size
            frame = cv2.resize(frame, None, fx=2, fy=2)
            vehicleframe = detection(frame)
            cv2.imshow('vehicle detection', vehicleframe)
        else:
            break
        if controlkey == ord('q'):
            break
    realtimevideo.release()
    cv2.destroyAllWindows()

capturescreen()