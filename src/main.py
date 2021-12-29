from cameraCapture import Video
#import droneMission
from fireClassifier import FireClassification
import cv2
from droneMission import start_mission
from droneMission import vehicle
from droneMission import get_location_offset_meters
import time
import threading

home = None
vehicle = None

def set_home(newHome):
    global home
    home = newHome

def get_home():
    global home
    return home


def set_vehicle(newVehicle):
    global vehicle
    vehicle = newVehicle


def get_vehicle():
    global vehicle
    return vehicle


def classify_fire():
    print("i func")
    while True:
        # Wait for the next frame
        if not video.frame_available():
            continue
        print("billede")
        frame = video.frame()
        print(f'main home = {home}')
        currentHome = get_home()
        if currentHome is None:
            continue
        wp = get_location_offset_meters(currentHome, 0, 0, 0)
        print(f'Current lat = {wp.lat}, current lon = {wp.lon}, current alt = {wp.alt}')

        # Todo - Use classifier on the frame above
        # If the frame/image gets classified as a fire image, ping the authorities.

        frame = cv2.resize(frame, (254, 254), interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    # Create the video object
    # Add port= if is necessary to use a different one
    training_location = "C:/Users/Sissel/PycharmProjects/Fire-Detection/Training"
    test_location = "C:/Users/Sissel/PycharmProjects/Fire-Detection/Test"
    #test_image = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data/Fire/resized_test_fire_frame1.jpg"
    model = "C:/Users/Sissel/PycharmProjects/Fire-Detection/saved_model/mymodel"

    # Load in the classifier, video stream, and mission classes.
    classifier = FireClassification(trainingSetLocation=training_location, testSetLocation=test_location, modelLocation=model)
    video = Video()
    #mission = DroneMission()
    """mission = DroneMission()

    # Start the drone mission
    #mission.start_mission()

    # Wait for the drone to have started the mission
    #time.sleep(10)
    time.sleep(10)"""


    # Start the drone mission on seperate thread
    #x = start_mission()
    #y = classify_fire()
    #time.sleep(60)
    print("inden drone tråd")
    droneThread = threading.Thread(target=start_mission, name="Bib")
    print("lavet drone tråd")
    fireThread = threading.Thread(target=classify_fire, name="Bob")
    print("starter drone")
    droneThread.start()
    print("før sleep")
    time.sleep(10)
    print("efter sleep")
    fireThread.start()



