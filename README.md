# UAV wildfire detection
## About the project
This project is a project submission for the subject DM884: Unmanned Aerial Vehicles at SDU. Detecting wildfires early can reduce the possible devastation the fires can cause; therefore a fire detection system to detect a wildfire early would prevent a possible big forest fire. This project will aim to create a fire detection drone that will hover over a specified area, and open a connection to a server that will receive images from the drone, and then perform classification on those images to if there is fire or not. If the server classifies an image as containing fire, it will print a message. As an extension, the server could ping the local fire department.

There are two parts of this project, a drone part, and a classification part. The drone part is inside /src/droneMission.py and the classification part is inside /src/fireClassifier.py. The whole project is run by running /src/main.py
## How to run the project
Running this project requires the user to have [PX4 Sitl](https://github.com/mavlink/qgroundcontrol/releases/download/v4.0.11/QGroundControl.AppImage), [QGroundControl](http://qgroundcontrol.com/), [Gazebo](http://gazebosim.org/) and [Dronekit](https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html) downloaded. The user is also required to have Python version 3.7 or newer. Inside PX4 we are using a modified version of the drone typhoon h480, to angle a camera downwards. 
This sdf file is located in /typhoonH480/typhoon\_h480, and should replace the sdf file /path/to/px4/models/typhoon\_h480/typhoon\_h480.sdf. 

After having met the requirements, start by having both QGroundControl (this should be started before Gazebo) and Gazebo running. The Gazebo should be started with the typhoon H480 drone, it can be started like this when inside the PX4-Autopilot folder:
```
make px4_sitl gazebo_typhoon_h480
``` 
Optionally it can be started with another world than the default one:
```
make px4_sitl gazebo_typhoon_h480__[Name of the world]
``` 
When everything is set up, the user can run the python file /src/main.py to start the project, like so:
```
python3 main.py
```
The drone will fly in a grid while having an open port on the camera. The script will then connect to the camera stream and perform classification on the images and print the predicted result.

skriv at QGroundControl ikke virker altid og fker dronen op, dronen vil ikke altid starte