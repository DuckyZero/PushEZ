# Author: Christopher Rossi
# Project Name: PushEZ - Push up Counter
# Start Date: 5/2/2021
# End Date: Ongoing
# Description: Verbal push up counter program which was designed to by-pass engine.runAndWait() lag with opencv
#              webcam display.

# Import dependencies
from csv import reader
import pyttsx3

# Variable setup
engine = pyttsx3.init()
num = []
curr = None

# Chance text-to-speech voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Loop through csv file and verbally announce the counter
while True:
    # open file in read mode
    with open('data.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        # row variable is a list that represents a row in csv
        for row in csv_reader:
            # if-statement by-passes blank spaces
            if len(row) > 0:
                if row[0] != 'counter':
                    # only voices the counter if the number is new otherwise skip
                    curr = row[0]
                    if curr not in num:
                        engine.say(row[0] + ' push up')
                        engine.runAndWait()
                        num.append(curr)


