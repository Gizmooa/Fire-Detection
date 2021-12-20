from cameraCapture import Video
from droneMission import DroneMission
from fireClassifier import FireClassification
import cv2
import time

if __name__ == '__main__':
    # Create the video object
    # Add port= if is necessary to use a different one
    training_location = "C:/Users/barth/Documents/Studie/Fire-Detection/classification"
    test_location = "C:/Users/barth/Documents/Studie/Fire-Detection/classification/test_data"
    test_image = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data/Fire/resized_test_fire_frame1.jpg"
    model = "C:/Users/barth/Documents/Studie/Fire-Detection/saved_model/mymodel"

    # Load in the classifier, video stream, and mission classes.
    classifier = FireClassification(trainingSetLocation=training_location)
    video = Video()
    """mission = DroneMission()

    # Start the drone mission
    mission.start_mission()

    # Wait for the drone to have started the mission
    time.sleep(10)"""

    while True:
        # Wait for the next frame
        if not video.frame_available():
            continue

        frame = video.frame()

        # Todo - Use classifier on the frame above
        # If the frame/image gets classified as a fire image, ping the authorities.

        frame = cv2.resize(frame, (254, 254), interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
