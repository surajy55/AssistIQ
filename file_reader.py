import pyttsx3

engine = pyttsx3.init("sapi5")

def speak(audio):
    print(audio)  # Print to terminal
    engine.say(audio)
    engine.runAndWait()

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # print(content)  # Print to console for debugging
            speak(content)  # Use the speak function to read the content
    except FileNotFoundError:
        response = "Sorry, I couldn't find that file."
        speak(response)
        print(response)
    except Exception as e:
        response = f"An error occurred: {e}"
        speak(response)
        print(response)
