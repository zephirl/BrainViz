#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pylsl import StreamInlet, resolve_stream

print("looking for Emotion stream...")
streamEmotion = resolve_stream('type', 'Performance-Metrics')
print("Motion stream found:",streamEmotion)


inlet = StreamInlet(streamEmotion[0])
sample, timestamp = inlet.pull_sample() # Input from Emotion
print("Emotion 00 seconds, timestamp: ", timestamp, sample) # Print 1st input


def EmotionCall():
    sample = inlet.pull_sample() # Input from Emotionsample, timestamp = inlet.pull_sample() # Input from Emotion
    #sample=[0,40,75,12,12,-1,12] # For debuging
    print(sample)
    
    calm,excitment,stress = EmotionStatus(sample[1],sample[2],sample[3],sample[4],sample[5],sample[6])
        
    calm = str(calm)
    calm = calm.replace(".", ",")
    
    excitment = str(excitment)
    excitment = excitment.replace(".", ",")
    
    stress = str(stress)
    stress = stress.replace(".", ",")
    
    print(calm,excitment,stress)
    
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
    # -1 indicates error
    calm = -1
    excitment = -1
    stress = -1
    
    # Evaluates Calmness
    if (En!=-1 and En<50 and Re!=-1) or (Re>60):
        calm = Re/100
    else:
        if (Re!=-1):
            calm = 0
        
    # Evaluates Excitment
    if (En>=50):
        excitment = (En/2-17)*3/100 # scale it as only from 50%
    else:
        if (En!=-1):
            excitment = 0
    
    # Evaluates Stress
    if (Ex>70):
        stress = ((Ex/2-25)*4)/100 # scale it as only from 70%
    else:
        if (Ex!=-1):
            stress = 0
    
    return calm, excitment, stress
    

while True:
    EmotionCall()


file.close()