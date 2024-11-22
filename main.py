import tkinter as tk
from tkinter import messagebox , filedialog ,font
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import datetime
import pyautogui
import random
import webbrowser
import wikipedia
import pywhatkit
import re
import threading
import time 
import sys
from dt import get_date_time
from NewsRead import latestnews
from health_info import healthinfo
from display import display_typing_effect
from code_generator import generate_code
from file_reader import read_file
from SEARCHNOW import searchGoogle, searchYoutube, searchWikipedia

# Initialization for pyttsx3
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)
   

lock = threading.Lock()

GREETINGS = [
    "hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis",
    "hey jarvis", "ok jarvis", "are you there"
]
GREETINGS_RES = [
    "Always there for you sir", "I am ready sir", "Your wish is my command",
    "How can I help you sir?", "I am online and ready sir"
]

NEWS_QUERIES = [
    "latest news", "what's the news", "tell me the news", "news update","read some news","breaking news","want to read some news",
    "news headlines", "any breaking news", "current news"
]

HEALTH_QUERIES = [
    "i have a health issue", "i am having a health problem", "i am feeling sick", "i am unwell", "i feel ill","not feeling well",
    "i am having a fever", "i have a fever", "i am not feeling well", "i have a health condition", "i am having health issues","i am not feeling"
]

GOOGLE_QUERIES = [
    "search on google", "google search", "look up on google", "find on google","google",
    "tell me about"
]

FILE_QUERIES =[
    "read file from path" ,"read file", "read the file" , "listen the file content" ,"read file content","read the file content"
]


YOUTUBE_QUERIES = [
    "play on youtube", "search on youtube", "find on youtube", "play video", "youtube video"
]

WEATHER_QUERIES = [
     "weather in", "current weather of", "climate in","weather" ,"climate"
]

# Introduction about Jarvis
JARVIS_INFO = """
I am JARVIS, Just A Rather Very Intelligent System. Created to assist you with various tasks,
from fetching information to controlling your applications. Feel free to ask me anything!
"""

# Responses about Jarvis' views on any topic
JARVIS_VIEWS = [
    "As an AI, my perspective is based on data and analysis. I can provide information on a wide range of topics.",
    "My views are objective, based on factual data and analysis.",
    "I am here to assist you with information and tasks, providing unbiased answers based on available data."
]

# Additional responses for varied interactions
ADDITIONAL_RESPONSES = {
    "who are you": JARVIS_INFO,
    "what are you": JARVIS_INFO,
    "introduce yourself": JARVIS_INFO,
    "your views on any topic": random.choice(JARVIS_VIEWS),
    "your opinion on": random.choice(JARVIS_VIEWS)
}

# Responses for different types of functions
FUNCTION_RESPONSES = {
    "google": [
        "Let me search that for you on Google.",
        "Searching on Google for you.",
        "Finding information on Google."
    ],
    "youtube": [
        "Opening YouTube for you.",
        "Let me find that video on YouTube.",
        "Playing your request on YouTube."
    ],
    "weather": [
        "Checking the weather for you.",
        "Fetching weather information.",
        "Let's see what the weather is like."
    ],
    "health": [
        "Let me check that for you.",
        "Looking into health information for you.",
        "Checking health data."
    ]
}

# Helper functions
def speak(audio):
    # with speak_lock:
    # print(audio)  # Print to terminal
        engine.say(audio)
        engine.runAndWait()
    # speech_queue.put(audio)

# def process_speech_queue():
#     """Continuously process speech requests from the queue."""
#     while True:
#         text = speech_queue.get()  # Get the next text item in the queue
#         engine.say(text)
#         engine.runAndWait()
#         speech_queue.task_done()  # Mark the task as done

# Start a background thread to process the speech queue
# speech_thread = threading.Thread(target=process_speech_queue, daemon=True)
# speech_thread.start()

def takeCommand():
    r = sr.Recognizer()
    query = None

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = r.listen(source, timeout=6)
        except sr.WaitTimeoutError:
            response="Listening timed out while waiting for phrase to start"
            log_response(response)
            speak(response)
            return "None"
        except Exception as e:
            print(f"Error while listening: {e}")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        response ="Sorry, I didn't recognize what you said"
        print(response)
        speak(response)
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"Error during recognition: {e}")
        return "None"

def cleanQuery(query):
    """Remove unnecessary prefixes from the query."""
    prefixes = ["jarvis", "google", "youtube", "wikipedia", "search", "on", "for"]
    # Create a regex pattern to match whole words only
    pattern = r'\b(' + '|'.join(prefixes) + r')\b'
    query = re.sub(pattern, '', query, flags=re.IGNORECASE).strip()
    return ' '.join(query.split())  # Remove any extra whitespace

def searchYoutube(query):
    """Search YouTube and play the first video."""
    with lock:
        query = cleanQuery(query)
        if query:  # Ensure that the query is not empty
            speak("This is what I found for your search!")
            pywhatkit.playonyt(query)
            speak("Playing the video now.")
        else:
            speak("Please provide a video title to search for.")

# def typing_effect(response):
#     sys.stdout.write("Jarvis: ")
#     sys.stdout.flush()

#     # Start the speaking in a separate thread so that it runs concurrently
#     speak(response)

#     for char in text:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         time.sleep(0.01)  # Short delay to speed up typing effect

#     print()  # Move to the next line after the response is complete

def log_response(response):
    print(f"Jarvis: {response}")

def startup():
    print("Initializing Jarvis")
    speak("Initializing Jarvis")
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    # current_time = datetime.datetime.now().strftime("%H:%M:%S")
    # speak(f"Currently it is {current_time}")
    print("I am online and ready sir. Please tell me how may I help you")
    speak("I am online and ready sir. Please tell me how may I help you")



def fetch_weather(city):
    api_key = "f00bafae4be0afd7190206d404dc9361"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Get temperature in Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        # print("API Response:", weather_data)

        if weather_data['cod'] == 200:  # Check if the request was successful
            return {
                'temperature': weather_data['main']['temp'],
                'weather_description': weather_data['weather'][0]['description'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed']
            }
        else:
            return None  # City not found or other error
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
    

def handle_command(query):
    query = query.lower()

    if query in GREETINGS:
        response = random.choice(GREETINGS_RES)
        speak(response)
        log_response(response)
        return False

    if "wake up" in query:
        response = "I am awake, sir."
        log_response(response)
        speak(response)
        return False 

    elif "go to sleep" in query:
        response = "Ok sir, you can call me anytime."
        log_response(response)
        speak(response)
        return True

    if "date" in query and "time" in query:
        response = get_date_time("date time")
        log_response(response)
        speak(response)
    elif "date" in query:
        response = get_date_time("date")
        log_response(response)
        speak(response)
    elif "time" in query:
        response = get_date_time("time")
        log_response(response)
        speak(response)



    elif any(word in query for word in FILE_QUERIES):
        response = "Please select the file "
        log_response(response)
        speak(response)

        # wait for user to enter the file path
        file_path = filedialog.askopenfilename(title="Select a file")
        
        if file_path:
            read_file(file_path)
        else:
            response = "No file selected."
            log_response(response)
            speak(response)

    elif "hello" in query:
        response = random.choice(GREETINGS_RES)
        log_response(response)
        speak(response)
    elif "i am fine" in query or "how are you" in query:
        response = "Perfect, sir"
        log_response(response)
        speak(response)
    elif "thank you" in query:
        response = "You are welcome, sir"
        log_response(response)
        speak(response)

    elif "pause" in query:
        pyautogui.press("k")
        response = "Video paused"
        log_response(response)
        speak(response)
    elif "play" in query:
        pyautogui.press("k")
        response = "Video played"
        log_response(response)
        speak(response)
    elif "mute" in query:
        pyautogui.press("m")
        response = "Video muted"
        log_response(response)
        speak(response)

    elif "volume up" in query:
        from keyboard import volumeup
        response = "Turning volume up, sir"
        log_response(response)
        speak(response)
        volumeup()
    elif "volume down" in query:
        from keyboard import volumedown
        response = "Turning volume down, sir"
        log_response(response)
        speak(response)
        volumedown()

    elif "open" in query:
        from Dictapp import openappweb
        openappweb(query)
    elif "close" in query:
        from Dictapp import closeappweb
        closeappweb(query)

    # elif any(word in query for word in GOOGLE_QUERIES):
    #     response = random.choice(FUNCTION_RESPONSES["google"])
    #     speak(response)
    #     log_response(response)
    #     searchGoogle(query)

    # elif any(word in query for word in YOUTUBE_QUERIES):
    #     response = random.choice(FUNCTION_RESPONSES["youtube"])
    #     speak(response)
    #     log_response(response)
    #     # Ensure only the actual search terms are passed
    #     cleaned_query = cleanQuery(query)  # Clean the query before passing it
    #     searchYoutube(cleaned_query)  # Pass the cleaned query directly

    elif "youtube" in query:
        searchYoutube(query)

    elif "tell me about" in query:
        person = query.replace("tell me about", "").strip()
        response = f"Searching information about {person}"
        speak(response)
        log_response(response)
        searchGoogle(person)
        
    elif any(word in query for word in WEATHER_QUERIES):

        if "in" in query:
            city = query.split("in")[-1].strip()
        elif "of" in query:
            city = query.split("of")[-1].strip()
        else:
            city = query.replace("weather", "").replace("what is the", "").strip()

        if city:
            weather_info = fetch_weather(city)  # Assuming this function fetches the weather data
            if weather_info:
                response = f"""
                The weather in {city} is currently {weather_info['weather_description']}.
                Temperature: {weather_info['temperature']} degrees Celsius.
                Humidity: {weather_info['humidity']}%
                Wind Speed: {weather_info['wind_speed']} km/h
                """
                log_response(response)  # Display the response in the console
                speak(response)
            else:
                speak(f"Sorry, I couldn't find weather information for {city}. Please try again.")
                print(f"Error: Couldn't find weather information for {city}.")
        else:
            speak("Please specify a city.")
            print("Please specify a city.")




    elif "temperature" in query:
        if "in" in query:
            city = query.split("in")[-1].strip()
        elif "of" in query:
            city = query.split("of")[-1].strip()
        else:
            city = query.replace("temperature", "").replace("what is the", "").strip()

        if city:
            search = f"temperature in {city}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            try:
                temp = data.find("div", class_="BNeawe").text
                response = f"The current temperature in {city} is {temp}."
                log_response(response)  # Display the response in the console
                speak(response)
            except Exception as e:
                speak("Sorry, I couldn't retrieve the temperature data.")
                print(f"Error: {e}")
        else:
            speak("Please specify a city.")
            print("Please specify a city.")


    elif "code" in query:

        if "in" in query:
            phrases_to_remove = ["write the code for", "the code for", "code for", "write code for"]        
            task = query.split("in")[0]  # Get the part of the query before "in"
            for phrase in phrases_to_remove:
                task = task.replace(phrase, "").strip()

            language = query.split("in")[-1].strip()  # Extract language from the query
            if not language:  # If no language is specified after "in"
                speak("Please specify the programming language.")
                print("Please specify the programming language.")
                
                # Keep asking for the programming language until the user provides it via voice
                while not language:
                    speak("What programming language would you like to use?")
                    language = takeCommand().strip()  # Use take_command to get voice input for the language
                    print(f"Detected language: {language}")

                    if not language:  # If still no language detected, prompt again
                        speak("I didn't hear any language. Please say it again.")

            # Generate code once the language is provided
            generated_code = generate_code(task, language)
            if generated_code:
                response = f"Here is the {language} code for {task}:\n{generated_code}"
                log_response(response)
                speak(response)
            else:
                speak("Sorry, I couldn't generate the code.")
                print("Error: Code generation failed.")
        
        else:
            speak("Please specify the programming language.")
            print("Please specify the programming language.")


    elif any(phrase in query for phrase in HEALTH_QUERIES):
        response = random.choice(FUNCTION_RESPONSES["health"])
        log_response(response)
        speak(response)
        healthinfo()  # Call the healthinfo function from health_info module

    elif any(word in query for word in NEWS_QUERIES):
        response = "Fetching the latest news..."
        speak(response)
        log_response(response)
        
        # Call latestnews function from NewsRead.py
        latestnews()  # This will internally prompt the user for country and category and fetch the news
        

    elif "finally sleep" in query:
        response = "Going to sleep, sir"
        speak(response)
        log_response(response)
        return True



    elif query in ADDITIONAL_RESPONSES:
        response = ADDITIONAL_RESPONSES[query]
        speak(response)
        log_response(response)
    
    else:
        response = "I'm sorry, I didn't quite get that. Can you please repeat?"
        log_response(response)
        speak(response)

    return False

def on_click():
    query = takeCommand()
    if query != "None":
        if handle_command(query):
            messagebox.showinfo("Sleeping", "The assistant is going to sleep.")
            root.quit()
    else:
        messagebox.showinfo("Try again", "Please say that again.")

# Setting up the GUI
# root = tk.Tk()
# root.title("Voice Assistant")

# canvas = tk.Canvas(root, height=300, width=400)
# canvas.pack()

# frame = tk.Frame(root, bg='white')
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# button = tk.Button(frame, text="Speak", padx=10, pady=5, fg="white", bg="#263D42", command=on_click)
# button.pack()


# Initialize root window
root = tk.Tk()
root.title("Voice Assistant")

root.geometry("500x400")


root.configure(bg="#f0f0f0")

# Canvas for background
canvas = tk.Canvas(root, height=400, width=500)
canvas.pack()


frame = tk.Frame(root, bg="#ffffff", bd=10, relief="solid", highlightthickness=2, highlightbackground="#a9a9a9")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.2)


button_font = font.Font(family="Helvetica", size=14, weight="bold")


button = tk.Button(frame, text="Speak", padx=20, pady=10, fg="white", bg="#4CAF50", font=button_font, relief="raised", bd=4, command=on_click)
button.pack(pady=20)


label = tk.Label(frame, text="Click to Speak", font=("Helvetica", 16, "italic"), bg="#ffffff", fg="#4CAF50")
label.pack()

# Add some padding around the frame for better aesthetics
frame.grid_propagate(False)

# Run startup function
startup()

root.mainloop()
