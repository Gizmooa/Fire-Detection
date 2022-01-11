# Fire Detection Drone
## About the project
This project is a project submission for the subject DM884: Unmanned Aerial Vehicles at SDU. Detecting wildfires early can reduce the possible devastation the fires can cause; therefore a fire detection system to detect a wildfire early would prevent a possible big forest fire. This project will aim to create a fire detection drone that will hover over a specified area, and open a connection to a server that will receive images from the drone, and then perform classification on those images too if there is a fire or not. If the server classifies an image as containing a fire, it will print a message. As an extension, the server could ping the local fire department.

There are two parts of this project, a drone part, and a classification part. The drone part is inside /src/droneMission.py and the classification part is inside /src/fireClassifier.py. The whole project is run by running /src/main.py. If the user wants to use the same pretrained model, as we have used for this project, it can be found on the [Google Drive](https://drive.google.com/drive/folders/1J3c1pT7mPxDns2ZT2wI2S1Z9SwDwLB9K). On this drive, there are located two models which are described in the report, alongside the data set used to train and test the model. 

For the current state of the program, we are using generic paths. If the user wants to use the training set, test set, or model. Then the training set should be placed in Fire-Detection/Training/, test set should be placed in Fire-Detection/Test/ and the model(s) should be placed in Fire-Detection/saved_model/. The model you want to use should be renamed mymodel. E.g., if you want to use the second model from the Google Drive, you'll have to rename the model to mymodel and place it in Fire-Detection/saved_model/. CAUTION, if you were to train a new model using the training data, the model in Fire-Detection/saved_model/mymodel will be overwritten. 

## How to run the project
Running this project requires the user to have [PX4 Sitl](https://github.com/mavlink/qgroundcontrol/releases/download/v4.0.11/QGroundControl.AppImage), [Gazebo](http://gazebosim.org/) and the dependencies listed in the dependency section. The user is also required to have Python version 3.7 or newer. Inside PX4 we are using a modified version of the drone typhoon h480, to angle a camera downwards. 
This sdf file is located in /typhoonH480/typhoon\_h480, and should replace the sdf file /path/to/px4/models/typhoon\_h480/typhoon\_h480.sdf. 

After having met the requirements, start by having Gazebo running. Gazebo should be started with the typhoon H480 drone, it can be started like this when inside the PX4-Autopilot folder:
```
make px4_sitl gazebo_typhoon_h480
``` 
Optionally it can be started with another world than the default one:
```
make px4_sitl gazebo_typhoon_h480__[Name of the world]
``` 
When everything is set up, the user can run the python file /src/main.py to start the project. 
```
python3 main.py
```
Optionally, the project can be started with the optional parameter "-he" to change the default height of 50.
```
python3 main.py -he 30
```
The drone will fly in a grid while having an open port on the camera. The script will connect to the camera stream and perform classification on the images. If the classifier detects any fires, a warning is printed on the terminal. Furthermore, the program saves the image of the fire with the GPS location of the drone and a timestamp. This can then be sent manually to the local fire department. 
## Dependencies
- tensorflow
- droneKit
- opencv
- numpy
- gi
- pymavlink
- matplotlib
- sktlearn
- seaborn
- argparse
- pathlib

## Known issues regarding QGroundControl
Initially, the project was built using QGroundControl as the ground controller for the project. However, QGroundControl accesses the camera which results in the port of the camera being occupied. This implies that the video capture class for this project cannot connect to the drone. Therefore, if the user wants to run the project with classification, QGroundControl either needs to be shut down or find a way to disable QGroundControl's access to the drone's camera. We tried multiple methods to disable QGroundControl's access to the camera, but without success. 
