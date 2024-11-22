import requests
import pyttsx3
import speech_recognition as sr
import webbrowser
from bs4 import BeautifulSoup
import json
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')
# Initialization for pyttsx3 (text-to-speech engine)
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    # print(audio)  # Print to terminal
    print(audio.encode('utf-8', errors='ignore').decode('utf-8'))
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=4)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"
        except Exception as e:
            print(f"Error while listening: {e}")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query.lower()  # Return the recognized query
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"Error during recognition: {e}")
        return "None"

def fetch_news_from_api(country, category):
    api_key = "9b998beccf4345609b55031820961f69"  # Replace with your actual API key
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    url = f"https://newsapi.org/v2/everything?q={category}+{country}&from=2024-10-28&sortBy=publishedAt&apiKey={api_key}"

    try:
        response = requests.get(url)
        news_data = response.json()
        if response.status_code == 200:
            articles = news_data.get("articles", [])
            return articles
        else:
            print(f"Error: {news_data.get('message', 'Unable to fetch news')}")
            return None
    except Exception as e:
        print(f"Error fetching news from API: {e}")
        return None

def fetch_news_from_google(query):
    try:
        search_url = f"https://www.google.com/search?q={query}&tbm=nws"
        webbrowser.open(search_url)
        speak(f"Here are some relevant news articles based on your query: {query}")
    except Exception as e:
        print(f"Error fetching news from Google: {e}")
        speak("Sorry, I couldn't fetch news articles from Google at the moment.")

def read_news(articles, max_headlines=5):
    if not articles:
        speak("I couldn't find any news articles based on your request. Let me search on Google.")
        return

    speak("Here are the latest news articles.")
    for idx, article in enumerate(articles[:max_headlines], start=1):
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        # content = article.get("content", "")
        # if content:
        #     content = content.split("[")[0]  # Remove any trailing content notes
        speak(f"Headline {idx}: {title}")
        speak(description)
        # if content:
        #     speak("Full article:")
        #     speak(content)
        if idx == max_headlines:
            break

def latestnews():
    speak("Which country's news would you like to hear? For example, India.")
    country = takeCommand()
    if not country or country == "none":
        speak("Sorry, I couldn't understand your request. Please try again.")
        return

    speak("Which category of news would you like to hear? For example, business, entertainment, health, science, sports, or technology.")
    category = takeCommand()
    if not category or category == "none":
        speak("Sorry, I couldn't understand your request. Please try again.")
        return

    # Attempt to fetch news from the News API
    articles = fetch_news_from_api(country, category.lower())

    if articles:
        read_news(articles, max_headlines=5)
    else:
        speak(f"I couldn't find any news articles related to {category} in {country}. Let me search for {category} news.")
        query = f"{category} news {country}"
        fetch_news_from_google(query)  # Fallback to Google News search

    speak("That's all the news for now.")

# If this file is executed directly, run the latestnews function
if __name__ == "__main__":
    latestnews()
