import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import requests
import pyjokes
import geocoder
import string

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Select a female voice if available
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
else:
    print("Female voice not found, using default voice.")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def get_current_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng  # Returns a list [latitude, longitude]
    else:
        return None

def get_weather(city_name=None):
    api_key = "bf0dd1a7acd4d40a290fb23cad3aefd5" 

    if city_name:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    else:
        
        location = get_current_location()
        if location is None:
            speak("Sorry, I couldn't determine your location.")
            return
        lat, lon = location
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        response = requests.get(url).json()
        print("API Response:", response)

        if response.get("cod") != 200:
            speak(f"Error: {response.get('message', 'Unable to retrieve weather data.')}")
            return

        weather = response['weather'][0]['description']
        temperature = round(response['main']['temp'] - 273.15, 2)  # Convert Kelvin to Celsius
        city = response.get('name', 'your location')
        speak(f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't retrieve the weather information.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def search_and_play(movie_name):
    matches = []

    # Get all available drives
    drives = [f"{drive}:\\" for drive in string.ascii_uppercase if os.path.exists(f"{drive}:\\")]

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if movie_name.lower() in file.lower() and file.endswith(('.mp4', '.mkv', '.avi')):
                    matches.append(os.path.join(root, file))

    if matches:
        speak(f"Found {len(matches)} match(es). Playing the first one.")
        os.startfile(matches[0])
    else:
        speak("Movie not found.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'tell a joke' in query:
            tell_joke()

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'get weather' in query:
            speak("Do you want the weather for your current location or a specific city?")
            choice = takeCommand().lower()
            if "current" in choice:
                get_weather()  # Use geolocation
            else:
                speak("Please tell me the name of the city.")
                city = takeCommand()
                if city != "None":  # Ensure valid input
                 get_weather(city_name=city)
                else:
                    speak("I couldn't understand the city name. Please try again.")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'play music' in query:
            music_dir = 'D:\\season'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'play' in query and 'movie' in query:
            speak("Which movie do you want to play?")
            movie_name = takeCommand()
            search_and_play(movie_name)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
            os.startfile(codePath)

        elif 'email to usman' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "muhammadusmananwar50@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend usman bhai. I am not able to send this email")    
        else:
            print("No query matched")
