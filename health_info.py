import json
import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Define the speak function
def speak(audio):
    print("\nJarvis:", audio)  # Log Jarvis's responses in the terminal with a newline
    engine.say(audio)
    engine.runAndWait()

def take_input(recognizer):
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio).lower()
        print("User Input (Voice):", user_input)
        return user_input
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Sorry, I'm having trouble accessing the Google API. Please check your internet connection.")
        return None
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
        return None

def healthinfo():
    speak("Sure, I can provide information on various health topics. What health condition are you experiencing?")
    
    recognizer = sr.Recognizer()

    # Allow user to provide input either verbally or via text
    user_input = take_input(recognizer)
    
    if not user_input:
        # Fallback to text input if voice input fails
        speak("I'm sorry, I didn't catch that. Please try again.")
        user_input = take_input(recognizer)
        # user_input = take_text_input()

    try:
        with open("cure.json", "r") as file:
            health_data = json.load(file)

        matching_diseases = []
        found_disease = None

        # Check if user input directly matches a disease name
        for disease in health_data["diseases"]:
            if user_input == disease["name"].lower():
                found_disease = disease
                break

        if found_disease:
            # Provide information for the found disease
            speak(f"You have selected {found_disease['name']} based on your input.")
            speak("Symptoms: " + ", ".join(found_disease["symptoms"]))
            speak("Categories: " + ", ".join(found_disease["categories"]))
            speak("Precautions: " + ", ".join(found_disease["precautions"]))
            if "allopathy" in found_disease:
                speak("Allopathy Cure: " + found_disease["allopathy"]["cure"])
            if "ayurveda" in found_disease:
                speak("Ayurveda Cure: " + found_disease["ayurveda"]["cure"])
            if "formulations" in found_disease:
                speak("Formulations: " + ", ".join(found_disease["formulations"]))
            if "herbs" in found_disease:
                speak("Herbs: " + ", ".join(found_disease["herbs"]))
        else:
            # Check for diseases matching the symptoms
            for disease in health_data["diseases"]:
                if any(symptom in user_input for symptom in map(str.lower, disease["symptoms"])):
                    matching_diseases.append(disease)

            if not matching_diseases:
                speak("Sorry, I couldn't identify the health condition based on your symptoms.")
                return

            if len(matching_diseases) == 1:
                found_disease = matching_diseases[0]
                speak(f"Based on your symptoms, you might be experiencing {found_disease['name']}.")
                speak("Symptoms: " + ", ".join(found_disease["symptoms"]))
                speak("Categories: " + ", ".join(found_disease["categories"]))
                speak("Precautions: " + ", ".join(found_disease["precautions"]))
                if "allopathy" in found_disease:
                    speak("Allopathy Cure: " + found_disease["allopathy"]["cure"])
                if "ayurveda" in found_disease:
                    speak("Ayurveda Cure: " + found_disease["ayurveda"]["cure"])
                if "formulations" in found_disease:
                    speak("Formulations: " + ", ".join(found_disease["formulations"]))
                if "herbs" in found_disease:
                    speak("Herbs: " + ", ".join(found_disease["herbs"]))
            else:
                speak("Based on your symptoms, it could be one of the following diseases:")
                for index, disease in enumerate(matching_diseases):
                    speak(f"{index + 1}. {disease['name']}")

                speak("Please say the name of the disease you want more information about.")
                # Capture user's choice via voice (disease name)
                choice = None
                while choice is None:
                    user_choice = take_input(recognizer)
                    if user_choice:
                        # Try to find the disease in the matching diseases list
                        user_choice = user_choice.strip().lower()
                        for disease in matching_diseases:
                            if disease["name"].lower() == user_choice:
                                found_disease = disease
                                choice = disease
                                break
                        if not choice:
                            speak("Sorry, I couldn't recognize that disease name. Please try again.")
                    else:
                        speak("I didn't catch that. Please say the disease name clearly.")

                # Provide information for the selected disease
                speak(f"You have selected {found_disease['name']}.")
                speak("Symptoms: " + ", ".join(found_disease["symptoms"]))
                speak("Categories: " + ", ".join(found_disease["categories"]))
                speak("Precautions: " + ", ".join(found_disease["precautions"]))
                if "allopathy" in found_disease:
                    speak("Allopathy Cure: " + found_disease["allopathy"]["cure"])
                if "ayurveda" in found_disease:
                    speak("Ayurveda Cure: " + found_disease["ayurveda"]["cure"])
                if "formulations" in found_disease:
                    speak("Formulations: " + ", ".join(found_disease["formulations"]))
                if "herbs" in found_disease:
                    speak("Herbs: " + ", ".join(found_disease["herbs"]))

    except sr.RequestError:
        speak("Sorry, I'm having trouble accessing the data.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")



