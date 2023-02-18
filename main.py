import traceback

import nltk
import wikipedia
import aiml
import pandas

#######################################################
# Initialise weather agent
#######################################################
import json, requests

from nltk import Expression, ResolutionProver, ResolutionProverCommand

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
#expr = Expression.fromstring("exists x.(company(x) & (contains(x, 'Nike') | contains(x, 'Adidas')))")
kb = []
data = pandas.read_csv('kb.csv',sep='\n', header=None)
[kb.append(read_expr(row)) for row in data[0]]
# read the knowledge base from a file

print (kb)
# Check for internal contradictions
#An empty list is used to prove in order to check if the knowledge base itself is consistent.
# If an empty list is consistent, then it means that the KB has no contradictions and is logically sound.
# This is a quick and simple way to check if t
# he KB is internally consistent before adding new expressions to it or
# using it for further reasoning.
try:
    prover = ResolutionProver()
    prover.prove([], kb)
    print('KB is consistent')
except Exception as e:
    print("error->",e)
    quit()

expr = read_expr("colorway(Air_Jordan_1_High, Red_and_Black)")
print(ResolutionProver().prove(expr, kb, verbose=True))

# main loop

while True:
    # get user input
    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    # pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    # activate selected response agent
    if responseAgent == 'aiml':
        answer = kern.respond(userInput)
    # post-process the answer for commands
    if answer[0] == '#':
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
            api_url = r"http://api.openweathermap.org/data/2.5/weather?q="
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
            succeeded = False;
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
            object, subject = params[1].split(' is ')
            expr = read_expr(subject + '(' + object + ')')
            # >>> ADD SOME CODES HERE to make sure expr does not contradict
            # with the KB before appending, otherwise show an error message.
            try:
                prover = ResolutionProverCommand(kb.append(expr))
                prover.prove()
                print(f'OK, I will remember that ')
            except:
                print('Error: contradiction found')

        elif cmd == 32:  # if the input pattern is "check that * is *"
            print(params)
            object, subject = params[1].split(' is ')

            expr = read_expr(subject + '(' + object + ')')
            print(expr)
            answer = ResolutionProver().prove(expr, kb, verbose=False)
            if answer:
                print('Correct.')
            else:
                print('It may not be true.')
                # >> This is not an ideal answer.
                # >> ADD SOME CODES HERE to find if expr is false, then give a
                # definite response: either "Incorrect" or "Sorry I don't know."

        elif cmd == 99:
            print("I did not get that, please try again.")
    else:
        print(answer)
