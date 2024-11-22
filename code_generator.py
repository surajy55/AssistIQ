import cohere

# Initialize the Cohere client with your API key
co = cohere.Client('rwNma4sHdH5KtgR0BtePKg2YOsvMCoyGQ5CYDFxB')  # Replace with your actual API key

def generate_code(task, language):
    """
    Function to generate code for a specified task in a given language.
    """
    prompt = f"Write {language} code for {task}."

    response = co.generate(
        model='command-r-plus-08-2024',  # Specify Cohere model type
        prompt=prompt,
        max_tokens=400,  # Adjust based on expected code length
        temperature=0.5  # Adjust for creativity
    )

    if response.generations:
        code_snippet = response.generations[0].text.strip()
        return code_snippet
    else:
        return "Sorry, I couldn't generate the code."
