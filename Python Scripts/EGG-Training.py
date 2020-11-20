"""
Processes EEG data from EEG headset (EPOC+) / Emotiv PRO app to Excel sheet
Averages EEG data received over a number of iterations (steps), (batch) times for more accurate results
Outputs data in excel sheet with name 'mode'
"""
"""
Version 1.1 // 19 Nov 2020 // Zephir Lorne
+ Added comments
+ Cleaned the code
"""

import time
import numpy as np
import pandas as pd
from pylsl import StreamInlet, resolve_stream   # To communicate with the EEG headset and Emotiv PRO app

# Print settings used for debugging more easily
np.set_printoptions(precision=3)    # Only .xxx
np.set_printoptions(linewidth=300)


### Initialization ###

# Resolve EEG streams on the lab network
print("looking for EEG stream...")
streamEEG = resolve_stream('type', 'EEG')
print("EEG stream found:",streamEEG)


inlet = StreamInlet(streamEEG[0]) # create a new inlet to read EEG data from the stream

# Check if data is received correctly by printing one sample
sample, timestamp = inlet.pull_sample() # Input from EEG
print("EEG 00 seconds, timestamp: ", timestamp, sample) # Print 1st input

init = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    # EEG data is received as arrays of 18 numbers
EEGlabels = ["1","2","3","AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4","0"]


# Countdown function to get ready
def countdown(count):
    print("Starting in...")
    for i in range(0,count):
        print(count-i)
        time.sleep(1)


# Averages EEG data received over a number of iterations (steps)
# Does it (batch) times for more accurate results
# Outputs data in excel sheet with name 'mode'
# Mode is a label you choose depending on tne activity you are doing
def train(mode,batches,steps):
    npSampleMode = np.append([EEGlabels],[init], axis=0)
    print("------",mode,"------")
    sample, timestamp = inlet.pull_sample() # Input from EEG
    print("00 seconds, timestamp: ", timestamp, sample) # Print 1st input

    # Number of averaged iteration batch to go over
    averageIterrations = batches
    averageCounter = 0

    # Number of values to average for each iteration batch
    stepIterrations = steps
    stepCounter = 0
    #sleepIncrements = 0.1

    while averageCounter < averageIterrations: # Iterates for number of averaged iteration batch to go over
        npSample = np.array(init) # Reset array used for average of batch
        stepCounter = 0 # Reset counter
        while stepCounter < stepIterrations:   # Iterates for number of values to average for each iteration batch
            sample, timestamp = inlet.pull_sample() # get a new sample
            npSample = np.add(npSample, np.array(sample)) # add npSample to array of data to average
            stepCounter += 1

        #print("sample: ",npSample)
        print("sample/20: ",npSample/stepIterrations) # print average data for batch
        npSampleMode = np.append(npSampleMode,[npSample/stepIterrations], axis=0) # add batch average data to 2D array of average datas for training type

        averageCounter += 1
        print(averageCounter," counter, timestamp: ", timestamp) # Note: timespent printed will be last of one of previous iteration

    print("sampleRelax1: ",npSampleMode) # print 2D array of average data

    df = pd.DataFrame(npSampleMode) # construct panada dataframe from np array
    print(df)
    filename = mode + ".xls"
    df.to_excel(filename, index=False, header=False) # save to Excel, exclude index and headers


def main():
    countdown(5)
    train("Relax",20,200)
    train("Stress",20,200)
    train("Relax2",20,200)
    train("Excite",20,200)


main()
