"""
Live processing of EEG data from EEG headset (EPOC+) / Emotiv PRO app
Detects head movements of user: left,right,forward,backward
Detects L/R eye blinking
Outputs/Updates these detections to text file every 0.5 seconds
"""
"""
Version 1.1 // 19 Nov 2020 // Zephir Lorne
+ Finished implementing Eye(), which detects if user blinks L/R eyes
+ Renamed functions
    + Separated motion() in two with Motion() and Angles()
    + CallMotion() is now ProcessData() which calls Motion() and Eyes() instead of only Motion()
+ Added beta calibration (not finished)
+ Added comments
+ Cleaned the code
+ Renamed file
"""
import time
import numpy as np
import pandas as pd
from squaternion import Quaternion      # To convert Quaternions into angles
from pylsl import StreamInlet, resolve_stream   # To communicate with the EEG headset and Emotiv PRO app

# Print settings used for debugging more easily
np.set_printoptions(precision=3)    # Only .xxx
np.set_printoptions(linewidth=300)


### Initialization ###

# Resolve EEG streams on the lab network
print("looking for EEG stream...")
streamEEG = resolve_stream('type', 'EEG')
print("EEG stream found:",streamEEG)

print("looking for Motion stream...")
streamMotion = resolve_stream('type', 'Motion')
print("Motion stream found:",streamMotion)

inlet = StreamInlet(streamEEG[0]) # create a new inlet to read EEG data from the stream
inlet2 = StreamInlet(streamMotion[0]) # create a new inlet to read Motion data from the stream

# Check if data is received correctly by printing one sample
sample, timestamp = inlet.pull_sample() # Input from EEG
print("EEG 00 seconds, timestamp: ", timestamp, sample) # Print 1st input

sample, timestamp = inlet2.pull_sample() # Input from Motion
print("EEG 00 seconds, timestamp: ", timestamp, sample) # Print 1st input

initMotion = [0,0,0,0,0,0,0,0,0,0,0,0,0]    # Motion data is received as arrays of 13 numbers

init = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    # EEG data is received as arrays of 18 numbers
EEGlabels = ["1","2","3","AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4","0"]

print("After calibration by Emotiv Pro, face the screen to calibrate as well here")

# Countdown function to get ready
def Countdown(count):
    print("Starting in...")
    for i in range(0,count):
        print(count-i)
        time.sleep(1)


# Reads EEG data from AF3_Left and AF4_Right inputs which see a spike
# When an the left or/and right eye closes/opens
# User can interact with the game (play a sound or pick/let go of an object by blinking one eye or the other)
# For each eye, return 1 if state changes (opens/closes) or 0 if state doesn't change
def Eyes():
    streamEEG = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streamEEG[0]) # create a new inlet to read EEG data from the stream
    sample, timestamp = inlet2.pull_sample() # Input from Motion

    AF3_Left = sample[3]    # AF3 corresponds to index 3 of array input
    AF4_Right = sample[14]  # AF4 corresponds to index 14 of array input

    left_eye = 0
    right_eye = 0

    # /!\ '40' Thresholds are to be adjusted
    if AF3_Left > 40:
        left_eye = 1
    if AF4_Right > 40:
        right = 1

    return left_eye,right_eye



# Determines if user wants to go left,right,forward,backward based on head angles
# For each axis, return 1 for movement or 0 for none
def Motion(angle1,angle2,angle3):
    left=0
    right=0
    forward=0
    backward=0

    # Thresholds need tuning depending on configuration
    if (angle2>-70):
        if angle1>45:
            backward=1
            print("backward")
        if angle1<-80:
            forward=1
            print("forward")
    else:
        if angle1>-60:
            left=1
            print("left")
        if angle1<-120:
            right=1
            print("right")

    return left,right,forward,backward


# Returns 3 angles for head position from headset Motion data
def Angles():
    streamMotion = resolve_stream('type', 'Motion') # Resolve stream
    inlet2 = StreamInlet(streamMotion[0])   # Create a new inlet to read Motion data from the stream
    sample, timestamp = inlet2.pull_sample() # Get a new sample with timestamp

    # Motion data is received as Quaternion
    # This converts quaternion to angles with degrees as units
    # The Q1,Q2,Q3,Q4 are at index 3,4,5,6 ofthe array input
    q = Quaternion(sample[3], sample[4], sample[5], sample[6])
    e = q.to_euler(degrees=True)

    # Processes/stores the angles correctly
    angles = []
    angles.append(e)
    angles = np.array(angles)
    angles.flatten()
    np.rint([angles])
    print(angles)

    # Angles are stored in an array, we return them separated
    return angles[0][0],angles[0][1],angles[0][2]


# Processes Motion Data from headset and outputs it to file
def ProcessData():
    angle1,angle2,angle3 = Angles() # Gets 3 angles of head position
    left,right,forward,backward = Motion(angle1,angle2,angle3) # Determines if user wants to go left,right,forward(head down),backward (head up) based on head angles
    print(left,right,forward,backward)

    left_eye,right_eye = Eyes() # Gets if L/R eyes open or close
    print(left_eye,right_eye)

    # Communicate data with other software like Unity in real time
    # Writes processed motion and eye data to text file, which will then be read by Unity
    try:
        file = open("Motion.txt","w")
        file.write(str(left_eye))
        file.write(";")
        file.write(str(right_eye))
        file.write(";")
        file.write(str(left))
        file.write(";")
        file.write(str(right))
        file.write(";")
        file.write(str(forward))
        file.write(";")
        file.write(str(backward))
        file.close()
    except:
        print("Error in writing file")


# Fetch and write new data every 0.5 seconds (you can modify the interval)
Countdown(5)
while True:
    ProcessData()
    time.sleep(0.5)


#### FUTURE FEATURE ####
# To calibrate headset Angles / Eye blinking
# Implementation not finished:
# The objective will be that once a session starts, a user moves its head left,right,forward,backward
# and blink the L/R eyes so that the thresholds are adjusted each time for each individual
'''
def Calibration(count):
    print("Starting calibration:")
    angleAverages = np.array([0,0,0])
    for i in range(0,count):
        print(count-i)
        time.sleep(1)
        angles = Angles()
        angleAverages = np.add(angleAverages, np.array(angles)) # add npSample to array of data to average
    angleAverages = angleAverages/count
    print("angleAverages",angleAverages)
    return angleAverages
# print("Look forward")
# calibratedAngle1,calibratedAngle2,calibratedAngle3 = calibration(2)
# print("Look left")
# leftCal,leftCal2,leftCal3 = calibration(2)
'''
