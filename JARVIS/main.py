# pylint: disable=unsubscriptable-object
from codeop import CommandCompiler
import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3 as p
import time
import requests
from bs4 import BeautifulSoup
import pyautogui
from requests import get 
import urllib.parse
import pywhatkit as kit
import sys
import json


engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate',130)
voices = engine.getProperty('voices')
print(voices)



def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_news(headlines_limit=3):
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in&'
           'apiKey=3dfc323dd6a245c6b800ec4b704d7722')

    try:
        response = requests.get(url)
        news = json.loads(response.text)

        counter = 0
        for new in news["articles"]:
            title = str(new["title"])
            description = str(new["description"])

            print(f"Title: {title}\nDescription: {description}\n")
            speak(f"Title: {title}")
            speak(f"Description: {description}")

            counter += 1
            if counter>=headlines_limit:
               break

        speak("Do you have any other work?")

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        speak("Sorry, I couldn't fetch the news.")


def get_weather(command):
    key = "a59077aff4b9adf26e85f034ed8e8ae7" 
    weather_url = "https://api.openweathermap.org/data/2.5/weather?"

    if "in" in command.split():
        location_index = command.split().index("in")
        location = ' '.join(command.split()[location_index + 1:])
        url = weather_url + "appid=" + key + "&q=" + location
        js = requests.get(url).json()

        if js["cod"] != "404":
            weather = js["main"]
            temperature = weather["temp"] - 273.15
            humidity = weather["humidity"]
            desc = js["weather"][0]["description"]
            wind_speed = js["wind"]["speed"]
            weather_response = f"The temperature in Celsius is {temperature:.2f}, The humidity is {humidity}%. The wind speed is {wind_speed} m/s, The weather description is {desc}."
            print(weather_response)
            speak(weather_response)
            return True
        else:
            speak("City not found")
    else:
        speak("Please specify a location for the weather.")

    
    return False


    
def takeCommand(command_type=None):
    user_response = ""
    if command_type == "google":
        speak("What should I search on Google?")
    elif command_type == "youtube":
        speak("What should I search on YouTube?")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 0.6)
        print("Jarvis is Listening...")
        audio = r.listen(source)

        try:
            print("Jarvis is Recognizing...")
            text = r.recognize_google(audio, language='en-in' or 'hi-in')
            print(f"User said: {text}")
            return text.lower()
       
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return takeCommand(command_type)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            speak("Sorry, I encountered an error. Please try again.")
            return "Some error occurred. Sorry from Jarvis"


def open_google(search_query):
    search_query_encoded = urllib.parse.quote(search_query)
    google_url = f"https://www.google.com/search?q={search_query_encoded}"

    speak(f"Searching on Google for {search_query}...")
    print(f"Searching on Google for {search_query}...")
    webbrowser.open_new_tab(google_url)
    time.sleep(7)
    speak("Do you have any other work?")
    user_response = takeCommand()


def open_youtube(search_query=None):
    if search_query is None:
        speak("What should I search on YouTube?")
        search_query = takeCommand(command_type="youtube")

    speak(f"Searching YouTube for {search_query} and playing the video...")
    kit.playonyt(search_query)
    time.sleep(5)

    speak("Do you have any other work?")
    user_response = takeCommand()


if __name__ == "__main__":
    print("Welcome To JARVIS AI")
    data = None
    temperature = None
    user_response = ""
    first_interaction = True
    while True:
        if first_interaction:
            speak("Hello there, I am your voice assistant Jarvis, how may I assist you?")
            first_interaction = False

        command = takeCommand()

        if "news" in command:
            get_news(headlines_limit=3)

        

        if "google" in command:
            search_query = takeCommand(command_type="google")
            open_google(search_query)

        elif "youtube" in command:
            search_query = takeCommand(command_type="youtube")
            open_youtube(search_query)

        elif "play music".lower() in command.lower():
            music_path = r'C:\Users\aryah\Downloads\JOXION - RPM [NCS Release].mp3'
            os.startfile(music_path)
            speak("Playing Music")
            print("Playing Music...")
            time.sleep(5)

        elif "the time".lower() in command.lower():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
            print(f"The current time is {current_time}")
            time.sleep(2)

        elif "ip address" in command.lower():
            ip = get('https://api.ipify.org').text
            speak(f"Your IP Address Is {ip}")
            print(f"Your IP Address Is {ip}")
            time.sleep(2)

        elif "switch the window" in command.lower():
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
            speak("Switching the window")
            print("Switching the window...")
            time.sleep(3)

        elif "start cmd" in command.lower():
            os.system("Start cmd")
            speak("Opening command prompt")
            print("Opening command prompt...")
            time.sleep(3)

        elif "weather" in command.lower():
            if get_weather(command):
                speak("Do you have any other work?")
                user_response = takeCommand()
            
                

        elif "no thanks" in command.lower():
            print("Debug: Exiting the program...")
            speak("Thank you for using me,  Have a good day.")
            sys.exit()