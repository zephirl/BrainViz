# BrainViz

[Repo currently being updated, it should be done by december]

## Inspiration
We wanted to create a video game that everyone even disabled and injured people with limited body movement range could play. 
## What it does
Hence we create a video game where the gamepad is a headset measuring brain activity. You control your character with emotions and small head movements and eye blinks.
## How we built it
We built it using unity, python, and an EEG headset.
## Challenges we ran into
Connecting and live streaming data from the headset to a python script was a challenge. Identifying the emotions only with the brain waves was very hard. And then connecting the python script to unity was a challenge. 
## Accomplishments that we're proud of
We are very proud of us having pushed through, even when it seemed impossible, having made a game that interacts with your emotions.
## What we learned
We have learned that link different hardware and languages is challenging but doable and that a lot of try and error is required as well as patience.
## What's next for BrainViz
We want to create a more accurate version of it with more emotions and a more complex videogame.


## Libraries used:
Emotiv lsl (to communicate between the brainware and the python script): https://github.com/Emotiv/labstreaminglayer/tree/master/examples/python


Squaternion (to convert quaternion data to angles, for movement): https://pypi.org/project/squaternion/


