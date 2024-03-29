#######################################################
# Initialise weather agent
#######################################################
import json
import random

import requests

import aiml
import pandas
import wikipedia
from nltk import ResolutionProver
from nltk.sentiment import SentimentIntensityAnalyzer
#
from nltk.sem.logic import *

from Fuzzy import MyFuzzy
from QandA import QnAMatcher
from SentanceAnalyser import SentenceAnalyser
from VoiceIO import TTS

# set voice io
speech_recognizer = TTS()
# set mute flag to false, this controls narration of outputs
muteFlag = True

fuzzer = MyFuzzy()
fuzzer.setSystem()

# custom sentence analyser function
SentenceAnalyser = SentenceAnalyser()


# sentiment analysis function and responses
def sentiment(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores["compound"]


positive_responses = [
    "Great job! Keep it up!",
    "You're doing great!",
    "You're a sneaker expert!",
    "You know your stuff!"
]
negative_responses = [
    "You need to improve.",
    "This is not good enough.",
    "You're making mistakes.",
    "You're not doing well."]


# output function that handles both tts and console outputs
def display(text):
    print(text)
    if muteFlag:
        speech_recognizer.repeat_speech(text)
    return


def objsplitter(objet):
    # check if object has multiple values in which case split then reformat and combine
    if ("," in object):
        words = object.split(",")
        words = [word.replace(" ", "_") for word in words]
        finalobject = ", ".join(words)
        print("-->" + finalobject)
        finalobject = finalobject.replace(", _", ", ")
        print("-->" + finalobject)
    else:
        finalobject = object.replace(" ", "_")
    return finalobject


# insert your personal OpenWeathermap API key here if you have one, and want to use this feature
APIkey = "5403a1e0442ce1dd18cb1bf7c40e776f"

#######################################################
#  Initialise AIML agent
#######################################################

# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.setTextEncoding(None)
# Use the Kernel's bootstrap() method to initialize the Kernel. The
# optional learnFiles argument is a file (or list of files) to load.
# The optional commands argument is a command (or list of commands)
# to run after the files are loaded.
# The optional brainFile argument specifies a brain file to load.
kern.bootstrap(learnFiles="mybot-basic.xml")
#######################################################
# Welcome user
#######################################################
print("Welcome to this chat bot. Please feel free to ask questions from me!")

# start knowledge base

read_expr = Expression.fromstring
# expr = Expression.fromstring("exists x.(company(x) & (contains(x, 'Nike') | contains(x, 'Adidas')))")
kb = []
data = pandas.read_csv('kb.csv', sep='\n', header=None)
[kb.append(read_expr(row)) for row in data[0]]
# read the knowledge base from a file

# Check for internal contradictions


if ResolutionProver().prove(None, kb, False):
    display("internal error with kb")
    quit()

# set voice flag to false
textInputFlag = True

# main loop

while True:
    # get user input
    # text input options
    if textInputFlag:
        try:
            userInput = input("> ")
        except (KeyboardInterrupt, EOFError) as e:
            print("Bye!")
            break
        if "_" in userInput:
            continue
        if userInput == "switch to voice":
            print("switching to voice")
            textInputFlag = False
            continue
    # voice input options
    else:
        userInput = speech_recognizer.speech_to_text()
        if userInput == "switch to text":
            textInputFlag = True
            continue

    if len(userInput) == 0:
        textInputFlag = True
        continue

    # pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    # activate selected response agent
    if responseAgent == 'aiml':
        answer = kern.respond(userInput)
    # post-process the answer for commands
    if answer[0] == '#':
        print(answer)
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            break
        elif cmd == 1:
            try:
                wSummary = wikipedia.summary(params[1], sentences=3, auto_suggest=False)
                print(wSummary)
            except:
                print("Sorry, I do not know that. Be more specific!")
        elif cmd == 2:
            succeeded = False
            api_url = r"https://api.openweathermap.org/data/2.5/weather?q="
            response = requests.get(api_url + params[1] + r"&units=metric&APPID=" + APIkey)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                if response_json:
                    t = response_json['main']['temp']
                    tmi = response_json['main']['temp_min']
                    tma = response_json['main']['temp_max']
                    hum = response_json['main']['humidity']
                    wsp = response_json['wind']['speed']
                    wdir = response_json['wind']['deg']
                    conditions = response_json['weather'][0]['description']
                    print("The temperature is", t, "°C, varying between", tmi, "and", tma, "at the moment, humidity is",
                          hum, "%, wind speed ", wsp, "m/s,", conditions)
                    succeeded = True
            if not succeeded:
                print("Sorry, I could not resolve the location you gave me.")

        elif cmd == 3:
            api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + params[1]
            response = requests.get(api_url)
            succeeded = False
            if response.status_code == 200:
                response_json = json.loads(response.content)
                if response_json:
                    t = response_json[0]
                    t = t.get("meanings")
                    t = t[0]
                    t = t.get("definitions")
                    t = t[0]
                    t = t.get("definition")

                    print("this is defined as" + t)
                    succeeded = True
            if not succeeded:
                print("Sorry, no definition can be found.")

        # price of *
        elif cmd == 4:
            print(params[1])


        # this will control how the chatbot interacts with the kb file
        # if input pattern is "I know that * is *"
        elif cmd == 31:
            object, subject = params[1].split(' IS ')
            # expr = read_expr(subject + '(' + object + ')')
            # >>> ADD SOME CODES HERE to make sure expr does not contradict
            # with the KB before appending, otherwise show an error message.
            # model(Air_Jordan_1, Air_Jordan_1_High)
            # if subject has multiple values
            print(subject)
            if "," in subject:
                print("subject can not have multiple values")
                continue
            else:
                final_subject = subject.replace(" ", "_")

            # check if object has multiple values in which case split then reformat and combine
            final_object = objsplitter(object)

            expr = read_expr(str(final_subject) + '(' + str(final_object) + ')')

            if (ResolutionProver().prove(None, kb + [expr], verbose=True)):
                print("this contradicts the kb")
            else:

                # exists x. (dog(x) & brown(x))
                # forall x. (dog(x) -> -brown(x))

                kb.append(expr)

                # add function that writes new kb to the file
                print('OK, I will remember that', object, 'is', subject)

        elif cmd == 32:  # if the input pattern is "check that * IS *"
            print(params)
            print(params[1])
            object, subject = params[1].split(' IS ')
            print(str(object))
            # if subject has multiple values
            if "," in subject:
                print("subject can not have multiple values")
                continue
            else:
                final_subject = subject.replace(" ", "_")

            # check if object has multiple values in which case split then reformat and combine
            final_object = objsplitter(object)
            expr = read_expr(str(final_subject) + '(' + str(final_object) + ')')
            print(expr)
            answer = ResolutionProver().prove(expr, kb, verbose=False)

            if answer:
                print('Correct.')
            else:
                # ADD SOME CODES HERE to find if expr is false, then give a
                # definite response: either "the opposite is true" or "Sorry I don't know."
                neg_expr = NegatedExpression(expr)
                if ResolutionProver().prove(neg_expr, kb, verbose=False):
                    print("the opposite is true")
                else:
                    print("Sorry I don't know")

        elif cmd == 33:
            print("my knowledge base is as follows:\n")
            for i in kb:
                print(i)
            print("i also have a fuzzy knowledge base")


        # fuzzy logic
        elif cmd == 35:

            query = None
            while query not in ["hype", "resale", "X"]:
                query = input("enter 'hype' or 'resale' predictor or X to return")

            if query != "X":

                flag = False
                while not flag:
                    args = input(
                        "Input brand_level, fit_level, price_level, style_level separated by commas in ranges 0 to 1: ")
                    args_list = args.split(",")
                    if len(args_list) != 4:
                        print("Please input exactly 4 arguments separated by commas.")
                        # You can choose to exit the program or ask for input again here

                    # Convert string arguments to floats
                    try:
                        brand_level, fit_level, price_level, style_level = map(float, args_list)
                    except ValueError:
                        print("Please input valid numbers in the range 0 to 1.")
                        # You can choose to exit the program or ask for input again here

                    # Check if arguments are in the range 0 to 1
                    if not all(0 <= arg <= 1 for arg in [brand_level, fit_level, price_level, style_level]):
                        print("Please input numbers in the range 0 to 1.")
                        # You can choose to exit the program or ask for input again here
                    else:
                        flag = True
                query_map = {"hype": "hype_level", "resale": "resale_value"}
                query = query_map[query]
                print(fuzzer.getFuzz(brand_level, fit_level, price_level, style_level, query))

        # ai/task c
        elif (cmd == 50 or cmd == 51):
            imagepath = input('enter image path')
            print(imagepath)
            # image recognition
            if cmd == 50:
                print("image recognition")
            # colour detection
            elif cmd == 51:
                print("colour detection")

        # no command found ==99
        elif cmd == 99:
            # use the cusom analyser that has been trained on corpus to workout what type of sentence

            sentencetype = SentenceAnalyser.classifier.classify(SentenceAnalyser.dialogue_act_features(params[1]))
            print(sentencetype)
            # if sentenece type is a question
            if "Question" in sentencetype:
                # search bow of words model
                matcher = QnAMatcher('sampleQA.csv')
                question, answer = matcher.find_similar_question(params[1])

                if (question and answer) is None:
                    display("I did not get that, please try again.")
                else:
                    display(question)
                    display(answer)

            elif "Statement" in sentencetype:
                # carry out sentiment analysis
                senty = sentiment(params[1])
                if senty > 0.2:
                    display(random.choice(positive_responses))
                elif senty < -0.2:
                    display(random.choice(negative_responses))
                else:
                    display("I did not get that, please try again.")
            elif "Greet" in sentencetype:
                display("hello")
            elif "Bye" in sentencetype:
                display("bye")
            else:
                display("I did not get that, please try again.")





    else:
        display(answer)
