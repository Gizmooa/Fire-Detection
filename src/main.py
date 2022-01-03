from cameraCapture import Video
from fireClassifier import FireClassification
import cv2
import droneMission
import time
import threading
import pathlib

def classify_fire():
    abs_path = str(pathlib.Path(__file__).parent.resolve())
    model = abs_path.replace("/src", "/saved_model/mymodel")

    #model = "/home/rasmus/Documents/Fire-Detection/src/saved_model/mymodel/"

    threshold = 0.2

    classifier = FireClassification(modelLocation=model)
    while True:
        # Wait for the next frame
        if not video.frame_available():
            continue
        frame = video.frame()
        currentHome = droneMission.home
        if currentHome is None:
            continue
        wp = droneMission.get_location_offset_meters(currentHome, 0, 0, 0)
        print(f'Current lat = {wp.lat}, current lon = {wp.lon}, current alt = {wp.alt}')

        frame = cv2.resize(frame, (254, 254), interpolation=cv2.INTER_AREA)
        predict_value = classifier.predict_image(frame)

        if threshold > predict_value:
            # TODO - Ping authorities as we've detected fire!
            print(f"[-] We've detected fire with the probability of {(1-predict_value)*100} percent")
        else:
            print(f"[+] No fire detected!")

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    abs_path = str(pathlib.Path(__file__).parent.resolve())
    # These generic paths requires the model, training and test folder to be placed in
    # the absolute path of the project(outside of src) and in the folder /Training, /Test/ and
    # saved_model/mymodel
    generic_model_location = abs_path.replace("/src", "/saved_model/mymodel")
    generic_test_location = abs_path.replace("/src", "/Training")
    generic_training_location = abs_path.replace("/src", "/Test")
    print(f"generic_model_location {generic_model_location}")
    print(f"generic_test_location {generic_test_location}")
    print(f"generic_training_location {generic_training_location}")
    
    training_location = "C:/Users/Sissel/PycharmProjects/Fire-Detection/Training"
    test_location = "C:/Users/Sissel/PycharmProjects/Fire-Detection/Test"
    #test_image = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data/Fire/resized_test_fire_frame1.jpg"
    model = "C:/Users/Sissel/PycharmProjects/Fire-Detection/saved_model/mymodel"
    # Load in the classifier, video stream, and mission classes.
    classifier = FireClassification(trainingSetLocation=generic_training_location, testSetLocation=generic_test_location, modelLocation=generic_model_location)
    video = Video()

    # Create two threads, one running the drone mission and another one
    # performing classification on images from the typhoon h480 drone.
    droneThread = threading.Thread(target=droneMission.start_mission, name="Bib")
    fireThread = threading.Thread(target=classify_fire, name="Bob")
    droneThread.start()
    fireThread.start()
    