import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import threading
import re

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Create a lock for thread safety
lock = threading.Lock()

def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

# def cleanQuery(query):
#     """Remove unnecessary prefixes from the query."""
#     prefixes = ["jarvis", "google", "youtube", "wikipedia", "search", "on", "for"]
#     for prefix in prefixes:
#         query = query.replace(prefix, "").strip()
#     return query
def cleanQuery(query):
    """Remove unnecessary prefixes from the query."""
    prefixes = ["jarvis", "google", "youtube", "wikipedia", "search", "on", "for"]
    # Create a regex pattern to match whole words only
    pattern = r'\b(' + '|'.join(prefixes) + r')\b'
    query = re.sub(pattern, '', query, flags=re.IGNORECASE).strip()
    return ' '.join(query.split())  # Remove any extra whitespace


def takeCommand():
    """Take voice command from user and return the recognized text."""
    r = sr.Recognizer()
    query = None

    with sr.Microphone() as source:
        print("Listening.....")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = r.listen(source, timeout=4)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error during recognition: {e}")

    return query.lower() if query else ""

def log_response(response):
    """Log responses to the terminal."""
    print(f"Jarvis: {response}")

def searchGoogle(query):
    """Search for a query on Google and speak the result."""
    query = cleanQuery(query)
    if query:
        log_response(f"This is what I found about {query} on Google")
        speak(f"This is what I found about {query} on Google")
        try:
            pywhatkit.search(query)
            result = wikipedia.summary(query, sentences=2)
            log_response(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Disambiguation error: {e}")
            log_response(f"Disambiguation error: {e}")
        except wikipedia.exceptions.PageError as e:
            speak(f"Page error: {e}")
            log_response(f"Page error: {e}")
        except Exception as e:
            speak(f"No speakable output available: {e}")
            log_response(f"No speakable output available: {e}")

def searchYoutube(query):
    """Search YouTube."""
    with lock:
        query = cleanQuery(query)
        if query:  # Ensure query is not empty
            pywhatkit.playonyt(query)
            speak("Playing the video now.")
        else:
            speak("Please provide a video title to search for.")

def searchWikipedia(query):
    """Search for a query on Wikipedia and speak the result."""
    if "wikipedia" in query:
        speak("Searching from Wikipedia....")
        log_response("Searching from Wikipedia....")
        query = cleanQuery(query)
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia..")
            log_response("According to Wikipedia..")
            print(results)
            speak(results)
            log_response(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Disambiguation error: {e}")
            log_response(f"Disambiguation error: {e}")
        except wikipedia.exceptions.PageError as e:
            speak(f"Page error: {e}")
            log_response(f"Page error: {e}")
        except Exception as e:
            speak(f"No speakable output available: {e}")
            log_response(f"No speakable output available: {e}")

if __name__ == "__main__":
    query = takeCommand()
    if query:
        log_response(f"User: {query}")
        if "google" in query:
            searchGoogle(query)
        elif "youtube" in query:
            searchYoutube(query)
        elif "wikipedia" in query:
            searchWikipedia(query)
