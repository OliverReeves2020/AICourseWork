import speech_recognition as sr
import pyttsx3


class TTS:
    def __init__(self, voice_name="fred"):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.set_voice(voice_name)
        self.recognizer = sr.Recognizer()

    def set_voice(self, voice_name):
        for voice in self.voices:
            if voice.name == voice_name:
                self.engine.setProperty('voice', voice.id)
                break

    def repeat_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Speak something...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print("You said:", text)
            self.engine.say("You said: " + text)
            self.engine.runAndWait()
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said")
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: {0}".format(e))
