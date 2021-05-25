# PushEZ
Pushup counter program to count and verbally annouce your push up repetition so you don't have to! This was built using a pre-built AI pose estimation model, object detection, and a python text-to-speech engine.

## Why It Was Built:

In the summer of 2020, a ton of people were stuck in lockdown and with nothing else to do people turned to exercising to help pass the time, relieve mental stress, and to better themselves physically. With all this exercising there will be repetition counting.... ew. Doing math while exercising is the last thing anyone wants to do, causing a lot of mental stress on a person. This results in you not putting in 100% into that workout. Until today that is! I was tired from all this arithmetic while wokring out and I planned to solve this issue with the power of programming! Look below for a quick preview:

![pushup_couter_github](https://user-images.githubusercontent.com/61894684/119556774-05b49780-bd65-11eb-99cb-c8818a47e912.gif)

[View video with audio click this!](#video-with-audio)

## How It Was Built:

This program was made with the programming language Python along with a few frameworks such as OpenCV for real-time computer vision, MediaPipe a pre-built AI pose estimation model and Pyttsx3 a text-to-speech engine. The full list of languages & frameworks are listed below:

* Python
* OpenCV
* Mediapipe (AI Pose Estimation Model)
* Pyttsx3
* Numpy
* CSV

## Use it yourself!

To start, install the lastest version of python and the following frameworks using PIP or Conda install:

```
pip install opencv-python
pip install mediapipe
pip install pyttsx3
pip install numpy
pip install csv          
```

After you install all the needed languages & frameworks. Copy the files into your IDE (Visual Stuido Code, Pycharm, etc.). Plug in a functional webcam (if you have multiple webcams plugged in you may need to change the camera code 0 to a 1 or 2 in pushup_counter.py, look below for an example).

```
cap = cv.VideoCapture(0) <-- change the number to 1 or 2 
```
Once your files and webcam are setup, you can now run the files. To do this, run pushup_counter.py in your IDE and then run voice.py in your SHELL, command prompt, or conda promt (for more information as to why we need to run these files seperate please refer to Project Roadblocks). Now you should be able to use the push up counter at full capacity to maximize your workouts!

## Project Roadblocks:
When creating this project, there was a few barriers that I had to overcome to make the project work as I envisioned it to be. The first blockage being the text-to-speech framework pyttsx3, this line of code caused a few issues: 
```
engine.runAndWait()
```

engine.runAndWait() caused a visual delay issue with the OpenCV webcam whenever this line of code was run. I tried a few techniques such as **threading** and **parallel programming** to get this to not delay the visual feed, however, it still had a delay. So my last option was to create a seperate python file (voice.py) where it loops through a csv file contained with push up counts and voices each correct push up and does not repeat any of the same numbers.

The second blockage was finding a framework to help assist with push-up detection. Before I found MediaPipe, I used OpenCV to do background subtraction to show white pixel outline of my body, which I could calculate the average of those pixels and then graph that data to form a nice sinusoidal curve where the peaks of those curves are a push up. However, the graph was very inaccurate (used MatPlotLib) and the peak identification algorithm I used did not identify all the peaks within the live graph. This made me wonder if there was an easier way, then I found MediaPipe pose estimation model which directly outlines shoulders, elbows, and wrist points on someones body, this made calculating joint angles easier.

## Future Improvements:
Some of the future improvements/features I would add to this program are listed below:
* Add an input system for the user to add their custom up/down push up position coordinates
* Made a .exe file for users to directly download and use the program without to much setup needed
* Make the MediaPipe AI pose detection/tracking confidence more so it will focus on their body and not their surroundings, making it more accurate.  

## Video With Audio:
https://user-images.githubusercontent.com/61894684/119557227-85dafd00-bd65-11eb-903b-704685990eda.mp4

## Citing:
* Calculating angle formula I modified to fit numpy: https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
* AI pose estimation documentation: https://google.github.io/mediapipe/solutions/pose.html
* Text-to-speech engine documentation: https://pyttsx3.readthedocs.io/en/latest/engine.html

