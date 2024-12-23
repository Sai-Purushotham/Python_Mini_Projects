import os
import pyttsx3
import speech_recognition as sr
import tkinter.messagebox as tmessage
import wolframalpha
from os.path import exists

# Speech recognition and text-to-speech setup
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

wolfprimealpha_app = input('Enter the API Token: ')


def audio(audio_text):
    """Text-to-speech conversion."""
    engine.say(audio_text)
    engine.runAndWait()


def welcomeInst():
    """Welcome and instruction messages."""
    print('Welcome to Calculator :)')
    audio('Welcome to Calculator :)')
    print('If you want to calculate something, please say something clearly')
    audio('If you want to calculate something, please say something clearly.')



def _takeCommand():
    """Take voice input from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        audio("Listening...")
        r.pause_threshold = 2
        r.energy_threshold = 3000
        try:
            audio_input = r.listen(source)
            print("Recognizing...")
            audio("Recognizing...")
            query = r.recognize_google(audio_input, language='en-IN')
            print(query)
            return query
        except Exception as e:
            tmessage.showinfo('Error', f'{e}')
            print("Didn't understand you...\nCan you repeat?...")
            return "NONE"


def _calculate(spech):
    """Perform the calculation based on user input."""
    try:
        client = wolframalpha.Client(wolfprimealpha_app)
        indx = spech.lower().split().index('calculate')
        query = spech.split()[indx + 1:]
        res = client.query(' '.join(query))
        answerr = next(res.results).text

        # Save to history file
        space = '\n'
        ourQuery = ' '.join(query)
        Question = 'Your Query was: '
        Answer = 'Your Answer was: '
        finalAnswer = Question + ourQuery + space + Answer + answerr + space

        file_path = './Voice Calculator/maths.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'a', encoding='utf-8') as mth:
            mth.write(finalAnswer)

        print("The answer is " + answerr)
        audio("The answer is %s" % answerr)

    except Exception as e:
        tmessage.showinfo('Error', f'Error calculating: {e}')
        print("Error calculating:", e)


# Welcome the user
welcomeInst()

# Main loop
while True:
    spech = _takeCommand().lower()

    if 'calculate' in spech:
        _calculate(spech)

    elif 'clear' in spech:
        file_path = './Voice Calculator/maths.txt'
        if exists(file_path):
            with open(file_path, 'r+') as file:
                file.truncate(0)
            print('History cleared.')
        else:
            tmessage.showinfo('Error', 'No history file exists.')

    elif 'history' in spech:
        file_path = './Voice Calculator/maths.txt'
        if exists(file_path):
            os.system(f'notepad {file_path}')
        else:
            tmessage.showinfo('Error', 'No history file exists.')

    elif 'quit' in spech or 'exit' in spech:
        audio("Goodbye!")
        quit()

    else:
        tmessage.showinfo('Oops', "Didn't understand.")
        print("Didn't understand.")
