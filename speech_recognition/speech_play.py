
import os

def speak(text):

    command = 'espeak "{}"'.format(text)

    os.system(command)


