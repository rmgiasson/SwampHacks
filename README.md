# SwampHacks X

## Description

Personal Pianist is a tool for aspiring beginner musical students, especially those interested in building foundational skills. The application offers a broad array of songs, allowing the user to enter and learn any song imaginable. Several young adults and children form their interest off learning new instruments off their love for popular music and while resources exist, there is no modern autonomous method to actually learn these pop songs. Thus, we have created an application where users can transcribe any file into piano notes, supplemented by sheet music and a visual guide. This is great for younger students who would improve their skills from following along on their own instrument while more experience instrumentalists can explore any song they would like to.

## Installation Guide

In developing this application our team used many libaries and dependencies that often clashed with another. For this implementation, we used Python version 3.8.

Libraries can be installed using 

```pip install spleeter django music21 os librosa```

Additionally, to convert MIDI files to visually palatable sheet music, we used MuseScore 4 which can be installed [here](https://musescore.org/en/download) and added to environment variables for usage.

For usage for node libraries, simply use 

```npm install```

to use all the libraries. Finally, to operate the code navigate into "ui" and "server/myproject" and use 

```npm start```

and

```python manage.py runserver```

This should activate the front end and backend respectively. 

Good luck on your music learning journey!!!
