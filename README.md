DRAMA 4598 Robot
Overview
This section is intended to give an understanding of the scenery robot's design from high-level control to hardware implementation and intended user control. The overview is written as if the system has been fully implemented and details of which parts of this project are completed and which are left to be implemented after January 15th, 2016 will be included in the 'Still to Come' section below. 
The scenery robot project allows a user to control a platform robot via an xbox controller and to record its motions for playback controlled from a user-friendly computer application. This is intended to be used in a performance such that the environment may move autonomously instead of being moved manually by people. The playback feature is intended to be accurate within inches and is intended to return to one of two 'home bases' offstage to recalibrate to an exact location using additional sensors. For safety, several emergency stops were included and are easy to access.	
To control the system, a computer program was created (more info in GUI section below). When the program is started, an interface appears to a user allowing him or her to make appropriate connections to a controller or server. The program does not necessarily need a controller to be connected in order to move, however without a controller, there must be previously recorded data for a specified path (see 'Queues' for more information on these saved paths). Once the proper connections have been made, the robot will be in one of a number of different modes. These modes depend on whether a path is being created (recorded), a path is being recreated (playing back), a user is simply manually controlling the robot, or the robot is not moving, either fully disconnected or only connected to a network and not a controller (see 'Robot Modes' for more info on these modes). The robot communicates with the system using both UDP and TCP to link computer control to a wifi network which interfaces with an arduino microcontroller (see communication for more information). 
In order to save and play back the paths, two encoder wheels were placed on the robot. These encoders track the movement of the robot by sampling the number of 'ticks' (which link directly to distance traveled) of both the left and right wheels over small increments. These time increments can be thought of as a sample rate with right and left wheel 'ticks' being sampled. The samples are continually sent back to the computer in TCP packets so the arduino does not have to store too much information and so this data can be saved on the computer. All queues for one production are saved in a file (see Queues for more information). Several different programs were used in this system and are specified in 'Code Structure' below. 

Hardware and Electronics
An arduino mega was used to control the robot. Two SEEED Studio W520 Ethernet Shields were used for communicating information to and from the computer. A bug was found in the use of the mega in which exclamation points could not be included in the serial outputs. PWM (Pulse Width Modulation) is used to control the wheels. The values powering the motor are in the range -127 to 127 where negative values are backwards. Two encoders were used to track the movements of the wheels which each produced 600 pulses (or ticks) in one 360 degree revolution. These encoder ticks are communicated back to the computer to be stored in a list. In playback, the paths are recreated by using such stored lists to recreate the PWM values supplied to the wheels over time, allowing the robot to follow the same path.
Hall effect sensors were used to position the robot back at the home base.
Communication
UDP was used to send data to the robot since fast communication was desired. TCP was used to send data back, since it was important that the path be saved precisely. In playback mode, TCP was favored to recreate the path precisely so this protocol is used to communicate to the robot. Packets being sent to the robot included UDP headers and 6 bytes of data, specifying time in 4 bytes and 2 bytes for integer values in the range of -127 to 127 for both wheels. Data sent back via TCP was of a similar form.

Robot Modes
Disconnected - nothing is communicating with the robot. This means the server is not connected - any xbox controller data to the computer would be meaningless.
Server only - the xbox controller is not connected but the server is. If queues exist, they can be used to control the robot.
Manual - the xbox controller is controlling the robot in real time and the encoder data is not being saved.
Recording - the xbox controller controller is controlling the robot in real time and the encoder data IS being saved.
Playback - using saved encoder data for a path (created with xbox controller), a path is ACTIVELY being followed. 

Queues
Queues are stored as 2D lists in python using a save_new_queue function. The lists hold first a queue name in index 0 (second element NULL) followed by pairs of encoder values in the form <left_encoder_number, right_encoder_number> in the remaining indices. All lists are stored in one text file and are separated by an empty '\n' line (additional lists are appended to the file). The function load_queue_file takes a text file storing the queues in this prescribed form as its parameter and makes a list of lists in python containing each of these queues (paths) so that they can all be loaded for reference in the GUI at once. An example of a loaded queue file is as follows:
queue1
[1, 2]
[2, 3]
[3, 4]

queue2
[1, 2]
[2, 3]
[3, 4]

queue3
[1, 2]
[2, 3]
[3, 4]

Once a queue file is recorded or a queue file is loaded, it will appear in the 'Queue' window in the interface. A user will be able to pick one of these queues and press the 'Go' button to recreate it. 
Controller Usage
The xbox controller was leveraged to work with a python file using an existing library. The y-direction of the left and right joysticks controls the speed of the left and white wheels, respectively. The raw values for each joystick are in the range of -0.5 to 0.5 and are not only scaled to the range -127 to 127 but also are adjusted for sensitivity around 0. This sensitivity value is in the range 0 to 1 can be changed; at 0 the data maps linearly and at 1 the scaling is much more skewed. 
GUI

The GUI was created in PyQt Designer and a screenshot of the display is shown above. First, in the top row indicators are included for easy status updates. The first, 'Path Status' is included as an indicator that some sort of an issue has occurred. The system cannot indicate all issues accurately so the language was chosen so that a user will not falsely assume system is working properly (as opposed to if the indicator read 'working' or 'not working') but will still be able to display an issue if one has been detected. The second indicator in the top row displays to the user which of the five modes that the robot is in (these modes are specified above in ' Robot Modes .' The third indicator shows whether the server connection is established between the robot and the computer.
Next the two large white spaces are for a list of path queues (left) and for a map of the stage. The queue window is a QListWidget which is scrollable and contains the names of the queues. If a user clicks on one of these queues and presses 'Go,' the robot will follow the path. The map provides an easy look at what the robot is attempting to navigate and ideally would update at different points in a production and would have a means of showing where the robot was on the stage at any given point.
Code Structure
Files: main.py, main_window_robot.py/ui, RoboControl.py, RoboNetwork.py, xinput.py/pyc. 
Other files for testing/not used yet: save_load_queues.py - a basic file for saving and loading a list of queues (these methods are included in main.py now), server_connect_dialog.py/pyc/ui - for user input of an IP address though currently this is hardwired.
Still to Come
Hardware and Electronics
An algorithm exists for ensuring that the robot has correctly returned to starting/ending position in the base with the hall-effect sensor, but it needs to be tested and expanded upon. 
Communication
Robot Modes
Queues
Controller Usage
GUI
'Progress bar', 'Time', and 'Time Left' all need to interface with the code. It is suggested that this be done by checking the current spot in the path queue (this will be an index in a list of encoder ticks for the left and right wheel) as a fraction of the total number of indices in the queue and translating that to a floored integer percentage. Calculating the total time of the path, path expired, etc can be done inAdditionally the software E Stops in the GUI are not functional as is.
File Structure
