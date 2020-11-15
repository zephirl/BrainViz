import time
import numpy as np
import pandas as pd
from squaternion import Quaternion
from pylsl import StreamInlet, resolve_stream
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=300)

# Resolve EEG streams on the lab network
print("looking for EEG stream...")
streamEEG = resolve_stream('type', 'EEG')
print("EEG stream found:",streamEEG)

print("looking for Motion stream...")
streamMotion = resolve_stream('type', 'Motion')
print("Motion stream found:",streamMotion)

inlet = StreamInlet(streamEEG[0]) # create a new inlet to read from the stream
inlet2 = StreamInlet(streamMotion[0])

sample, timestamp = inlet.pull_sample() # Input from EEG
print("EEG 00 seconds, timestamp: ", timestamp, sample) # Print 1st input

sample, timestamp = inlet2.pull_sample() # Input from Motion
print("EEG 00 seconds, timestamp: ", timestamp, sample) # Print 1st input

initMotion = [0,0,0,0,0,0,0,0,0,0,0,0,0]

# print("neutral")
# for i in range(0,2):
#         time.sleep(2)
#         streamMotion = resolve_stream('type', 'Motion')
#         inlet2 = StreamInlet(streamMotion[0])
#         sample, timestamp = inlet2.pull_sample() # get a new sample
        
#         q = Quaternion(sample[3], sample[4], sample[5], sample[6])
#         e = q.to_euler(degrees=True)
#         # print(e)
    
#         angles = []
#         angles.append(e)
#         angles = np.array(angles)
#         angles.flatten()
#         np.rint([angles])
#         print(angles)


init = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
EEGlabels = ["1","2","3","AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4","0"]


# # Countdown function to get ready
# def countdown(count):
#     print("Starting in...")
#     for i in range(0,count):
#         print(count-i)
#         time.sleep(1)


def eyes(AF3_Left,AF4_Right):
    left_eye = 0
    right_eye = 0
    if AF3_Left > 40:
        left_eye = 1
    if AF4_Right > 40:
        right = 1
    return left_eye,right_eye
        
def motion():
        left=0
        right=0
        forward=0
        backward=0
        print("motionnnnn")
        streamMotion = resolve_stream('type', 'Motion')
        inlet2 = StreamInlet(streamMotion[0])
        sample, timestamp = inlet2.pull_sample() # get a new sample
        
        q = Quaternion(sample[3], sample[4], sample[5], sample[6])
        e = q.to_euler(degrees=True)
        # print(e)
    
        angles = []
        angles.append(e)
        angles = np.array(angles)
        angles.flatten()
        np.rint([angles])
        print(angles)
        angle1 = angles[0][0]
        angle2 = angles[0][1]
        angle3 = angles[0][2]
        
        if (angle2>-70):
            if angle1>45:
                backward=1
            if angle1<-80:
                forward=1
        else:
            if angle3>60:
                left=1
            if angle3<30:
                right=1
            
        
        return left,right,forward,backward

def CallMotion():
    print("motionnn")       
    left,right,forward,backward = motion()
    print(left,right,forward,backward)
    try:
        file = open("Motion.txt","w")
        file.write("0")
        file.write(";")
        file.write("0")
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
    
count=100
def loop(count):
    print("Starting in...")
    for i in range(0,count):
        CallMotion()
        print(count-i)
        time.sleep(1)

loop(count)




# # Averages EEG data received over a number of iterations (steps)
# # Does it (batch) times for more accurate results
# # Outputs data in excel sheet with name 'mode'
# def train(mode,batches,steps):
#     npSampleMode = np.append([EEGlabels],[init], axis=0)
#     print("------",mode,"------")
#     sample, timestamp = inlet.pull_sample() # Input from EEG
#     print("00 seconds, timestamp: ", timestamp, sample) # Print 1st input
    
#     # Number of averaged iteration batch to go over
#     averageIterrations = batches
#     averageCounter = 0
    
#     # Number of values to average for each iteration batch
#     stepIterrations = steps    
#     stepCounter = 0
#     #sleepIncrements = 0.1
    
#     while averageCounter < averageIterrations: # Iterates for number of averaged iteration batch to go over
#         npSample = np.array(init) # Reset array used for average of batch
#         stepCounter = 0 # Reset counter
#         while stepCounter < stepIterrations:   # Iterates for number of values to average for each iteration batch
#             sample, timestamp = inlet.pull_sample() # get a new sample
#             npSample = np.add(npSample, np.array(sample)) # add npSample to array of data to average
#             stepCounter += 1
            
#         #print("sample: ",npSample)
#         print("sample/20: ",npSample/stepIterrations) # print average data for batch
#         npSampleMode = np.append(npSampleMode,[npSample/stepIterrations], axis=0) # add batch average data to 2D array of average datas for training type
    
#         averageCounter += 1
#         print(averageCounter," counter, timestamp: ", timestamp) # Note: timespent printed will be last of one of previous iteration
        
#     print("sampleRelax1: ",npSampleMode) # print 2D array of average data
    
#     df = pd.DataFrame(npSampleMode) # construct panada dataframe from np array
#     print(df)
#     filename = mode + ".xls"
#     df.to_excel(filename, index=False, header=False) # save to Excel, exclude index and headers
    
# countdown(5)
# train("Relax",20,200)
# train("Stress",20,200)
# train("Relax2",20,200)
# train("Excite",20,200)



    