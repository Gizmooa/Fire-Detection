from dronekit import Vehicle
from cameraCapture import Video
from fireClassifier import FireClassification
import cv2
import droneMission
import time
import threading
import pathlib
import argparse
import sys
from datetime import datetime


def classify_fire(fireClassifier):
    """
            Function that are run in main in a separate thread. It takes a trained classifier
            as a parameter, connects to the typhoon h480's camera and performs classification on the
            video stream from the typhoon h480's camera using the gst camera plugin.
            """
    # Threshold are a variable describing how accurate the classifier should be
    # on the prediction of fire, before alerting. Here, if the threshold is set to 0.2
    # the system will alert if the classifier are 80 percent sure there are fire.
    threshold = 0.2

    while True:
        # Wait for the next frame
        if not video.frame_available():
            continue
        frame = video.frame()
        currentHome = droneMission.home
        if currentHome is None:
            continue
        
        wp = droneMission.vehicle.location.global_frame

        print(f'Current lat = {wp.lat}, current lon = {wp.lon}, current alt = {wp.alt}')

        frame = cv2.resize(frame, (254, 254), interpolation=cv2.INTER_AREA)
        predict_value = fireClassifier.predict_image(frame)

        if threshold > predict_value:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            print(f"[FIRE DETECTED] We've detected fire with the probability of {(1-predict_value)*100} percent")
            print(f'[FIRE DETECTED] The fire were found at: lat = {wp.lat}, lon = {wp.lon}, alt = {wp.alt}')
            print(f'[FIRE DETECTED] The date and time of the fire found are: {dt_string}')
        else:
            print(f"[+] No fire detected!")

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or Vehicle.mission_is_done == True:
            break
        time.sleep(2)
        




if __name__ == '__main__':


    
    abs_path = str(pathlib.Path(__file__).parent.resolve())
    # These generic paths requires the model, training and test folder to be placed in
    # the absolute path of the project(outside of src) and in the folder /Training, /Test/ and
    # saved_model/mymodel
    model_location = abs_path.replace("/src", "/saved_model/mymodel")
    test_location = abs_path.replace("/src", "/Training")
    training_location = abs_path.replace("/src", "/Test")

    # Load in the classifier, video stream, and mission classes.
    classifier = FireClassification(trainingSetLocation=training_location,
                                    testSetLocation=test_location, modelLocation=model_location)
    video = Video()

    # Create two threads, one running the drone mission and another one
    # performing classification on images from the typhoon h480 drone.
    droneThread = threading.Thread(target=droneMission.start_mission, name="droneThread")
    fireThread = threading.Thread(target=classify_fire, args=(classifier,), name="fireThread")
    droneThread.start()
    fireThread.start()
    
