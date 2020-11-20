# BrainViz
BrainViz analyzes live brain activity to control a video game through your emotions, eye blinking and head movements:
Live processing of electroencephalogram data from EEG headset (EPOC+) & Emotiv PRO app.

[ Video demo coming soon ]


## Inspiration
We wanted to create an immersive and innovative experience accessible to everyone, including disabled and injured people with limited body movement.

## How it works
1. The EEG (electroencephalogram) headset detects the electrical activity in your brain.
2. This data is transferred live via Bluetooth to the computer.
3. The Emotiv PRO app (https://www.emotiv.com/emotivpro/) receives that data and sends it via the Lab Streaming Layer (LSL) protocol (https://github.com/Emotiv/labstreaminglayer/tree/master/examples/python).
4. The LSL data is received by the python scripts which then analyses and parse the data, summarized as such:
    + L/R eye blinking: detected with spikes from AF3 and AF4 EEG channels
    + Head movements: detected with headset accelerometer for left, right, forward, and backward movements
    + Emotions: Emotiv PRO app pre-analyzes EEG data to determine what emotions you feel. We re-analyze/parse this data to produce different behaviours depending on different emotion thresholds.
5. The analysis and interpretations from the python scripts are saved to a file multiple time per second.
6. Unity reads that file everytime it gets updated to update the game: the user is able to interact with the game with his brain only!

## Tools we used
+ Game engine: Unity (files will soon be made available on this repo)
+ Data analysis/processing: Python
  + Libraries used:
    + Emotiv LSL (to communicate between the brainware and the python script):
    + Squaternion (to convert quaternion data to angles, for movement): https://pypi.org/project/squaternion/
+ EEG headset: Emotiv Epoc+ (https://www.emotiv.com/epoc/)
+ EEG receiver: Emotiv PRO app (https://www.emotiv.com/emotivpro/)

## Challenges we ran into
Connecting and live streaming data from the headset to a python script and then to Unity was a real challenge.
Identifying the emotions only with the brain waves was very hard. We first tried to interpret the Raw EEG signals and their variation as we tried to feel different emotions but could not come to a simple formula/threshold, which is understandable given the limited timeframe we had and the complexity of electroencephalogram analysis. To solve this problem, we used the 'Performance-Metrics' data transmitted by the Emotiv PRO app to deal with the user's emotion.

## Accomplishments that we're proud of
We are very proud of us having pushed through, even when though it seemed impossible, having made a game that interacts with your brain and emotions is really cool!

## What we learned
We have learned that linking different hardware components and computer languages is challenging but doable. A lot of trial and error is required, as well as patience, but perseverance!
We've learned more about how our brains work as well.

## What's next for BrainViz
We want to create a more accurate version of it (by implementing some AI for EEG analysis), with more emotions, and a more complex and complete video-game.


Feel free branch/fork this repo!
