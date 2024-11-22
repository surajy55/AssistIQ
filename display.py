import threading
import pyttsx3
import pythoncom

def speak_text(text):
    """
    Use pyttsx3 to speak the text.
    :param text: The text to be spoken
    """
    pythoncom.CoInitialize()
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def display_typing_effect(output_text, label):
    """
    Display text character by character with a typing effect, while speaking and printing to the terminal.
    :param output_text: The text to display with typing effect
    :param label: The label widget to display the text on
    """
    # Printing the output to terminal as well
    print(output_text)

    label.config(text="")  

    # Start the speech in a separate thread
    threading.Thread(target=speak_text, args=(output_text,), daemon=True).start()

    # Typing effect function
    def type_character(index=0):
        if index < len(output_text):
            current_text = label.cget("text") + output_text[index]
            label.config(text=current_text)
            label.after(50, type_character, index + 1)

    # Start the typing effect
    type_character()
