"""import requests
url='https://stockx.com/en-gb'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
response = requests.get(url,headers)

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)"""

import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
"""fred Karen Jorge Luca Mariska """
for voice in voices:
    print(voice.name)
    if voice.name == 'fred':
        engine.setProperty('voice', voice.id)
        break


engine.say("i like bunsen burners")
engine.runAndWait()

"""

# Initialize the recognizer and engine instances
r = sr.Recognizer()

# Get input from the microphone
with sr.Microphone() as source:
    print("Speak something...")
    audio = r.listen(source)

# Convert speech to text
try:
    text = r.recognize_google(audio)
    print("You said:", text)

    # Convert text to speech
    engine.say("You said: " + text)
    engine.runAndWait()
except sr.UnknownValueError:
    print("Sorry, I could not understand what you said")
except sr.RequestError as e:
    print("Sorry, there was an error processing your request: {0}".format(e))

"""





