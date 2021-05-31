'''########################'''
''' T A L K I N G  B O T
    ''''''''''''''''''''
    libraries used: speech_recognition (to convert audio to text)
                    chatterbot (to implement a bot)
                    pyttsx3 (to convert text to speech)''' 
import speech_recognition as sr

from chatterbot import ChatBot

import pyttsx3 as pt

#defining function speak that converts text to audio
def speak(bot,text):
    engine= pt.init()
    voices=engine.getProperty('voices')
    engine.setProperty('rate',170)
    engine.setProperty("voice",voices[1].id) #setting voice to female voice(voices[1].id) for male voice set voices[0].id--(available indices are only 0 and 1)
    voices[1].age=20
    engine.say(text);
    print("\n",bot.name,": ",text)
    engine.runAndWait()
    engine.stop()

#defining function to hear what the user is saying
def speech(recognizer,microphone):
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("'microphone' must be 'Microphone' instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    response={
            "success":True,
            "error":None,
            "transcription":None
            }
    try:
        response["transcription"]=recognizer.recognize_google(audio)
    except sr.RequestError:
        ''' if the API was unavailable raising a connection error'''
        response["success"]=False
        response["error"]="Sorry!! Check your network connection. "
    except sr.UnknownValueError:
        response["error"]="Unable to recognize speech"
    return response


bot=ChatBot("Siris")
 
''' setting the trainer of our bot as ChatterBotCorpusTrainer'''
from chatterbot.trainers import ChatterBotCorpusTrainer
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train('chatterbot.corpus.english')


r=sr.Recognizer()
mic=sr.Microphone()
speak(bot,"Hi!!  I'm your talking bot, "+bot.name+". How can I help you?")
while(True):
    try:
        while(True):
            print("\nYou: ",end="")
            guess=speech(r,mic)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            speak(bot,"I didn't catch that. What did you say?\n") #if transcription is None and success is True then bot was unable to understand the audio.
        if guess["error"]:
            speak(bot,guess["error"])
            break
        print("{}".format(guess["transcription"]))
        message=guess["transcription"]
    
        if((message=='Bye')or(message=='bye')): #terminating bot when user says bye.
            reply="nice talking to you!! Bye."
            speak(bot,reply)
            break
        else:
            reply=bot.get_response(message)
            speak(bot,reply)
    except(KeyboardInterrupt,EOFError,SystemExit):
        break
