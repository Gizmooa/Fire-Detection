from cameraCapture import Video
#import droneMission
from fireClassifier import FireClassification
import cv2
from droneMission import start_mission
from droneMission import vehicle
import time
import threading

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
    droneThread = threading.Thread(target=start_mission())
    droneThread.start()


    while True:
        # Wait for the next frame
        if not video.frame_available():
            continue

        frame = video.frame()

        currentHome = droneMission.home
        wp = droneMission.get_location_offset_meters(currentHome, 0, 0, 0)

        print(f'Current lat = {wp.lat}, current lon = {wp.lon}, current alt = {wp.alt}')

        # Todo - Use classifier on the frame above
        # If the frame/image gets classified as a fire image, ping the authorities.

        frame = cv2.resize(frame, (254, 254), interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
