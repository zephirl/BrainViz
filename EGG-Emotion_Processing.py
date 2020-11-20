"""
Live processing of Emotion EEG data from EEG headset (EPOC+) / Emotiv PRO app
The Emotiv PRO app has a feature that analyzes EEG data to determine what emotions you feel
This script parses this data and triggers action depending on different thresholds of different emotions
It writes the output to a file every 10 seconds with new data
"""
"""
Version 1.1 // 19 Nov 2020 // Zephir Lorne
+ Added comments
+ Cleaned the code
+ Renamed file
"""

from pylsl import StreamInlet, resolve_stream   # To communicate with the EEG headset and Emotiv PRO app

# Resolve EEG streams on the lab network
print("looking for Emotion stream...")
streamEmotion = resolve_stream('type', 'Performance-Metrics')
print("Motion stream found:",streamEmotion)


inlet = StreamInlet(streamEmotion[0])   # create a new inlet to read EEG emotion data from the stream

# Check if data is received correctly by printing one sample
sample, timestamp = inlet.pull_sample() # Input from Emotion
print("Emotion 00 seconds, timestamp: ", timestamp, sample) # Print 1st input


def ProcessData():
    sample = inlet.pull_sample() # Input from Emotionsample, timestamp = inlet.pull_sample() # Input from Emotion
    #sample=[0,40,75,12,12,-1,12] # For debuging
    print(sample)
    print("testttt")
    sample = sample[0]
    print(sample)
    calm,excitment,stress = EmotionStatus(sample[1],sample[2],sample[3],sample[4],sample[5],sample[6])

    calm = str(calm)
    calm = calm.replace(".", ",")

    excitment = str(excitment)
    excitment = excitment.replace(".", ",")

    stress = str(stress)
    stress = stress.replace(".", ",")

    print(calm,excitment,stress)

    # Communicate data with other software like Unity in real time
    # Writes processed emotion data to text file, which will then be read by Unity
    try:
        file = open("Emotion.txt","w")
        file.write(calm)
        file.write(";")
        file.write(excitment)
        file.write(";")
        file.write(stress)
        file.close()
    except:
        print("Error in writing file")


def EmotionStatus(En,Ex,Fo,In,Re,St):
    # -1 indicates error: no data received from headset
    calm = -1
    excitment = -1
    stress = -1

    # The following thresholds have to be adjusted for each User
    # A calibration will be proposed in the future
    # You can choose to output either all or none response or scaled (uncomment the one wanted)

    # Evaluates Calmness
    if (En!=-1 and En<0.65   and Re!=-1) or (Re>60):
        #calm = Re/100
        #calm = Re
        calm=1
        print("Calm")
    else:
        if (Re!=-1):
            calm = 0

    # Evaluates Excitment
    if (En>=0.52):
        #excitment = (En/2-17)*3/100 # scale it as only from 50%
        #excitment = En
        excitment = 1
        print("excitment")
    else:
        if (En!=-1):q
            excitment = 0

    # Evaluates Stress
    if (Ex>0.45 ):
        #stress = ((Ex/2-25)*4)/100 # scale it as only from 70%
        #stress = Ex
        stress=1
        print("stress")
    else:
        if (Ex!=-1):
            stress = 0

    return calm, excitment, stress


# Emotion data from headset gets received at a frequency of 0.1Hz
# Thus we have new data every 10 seconds
while True:
    ProcessData()
