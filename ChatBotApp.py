# ChatBotApp.py
# Starter code for Python Chat Bot Program
# CIT-95 (Mohle) Spring 2024
# last updated: 4/24/24 by dH
# Suggested things to do:
#   Add chat memory
#   Use a local server like streamlit
#   Modify streamlit with HTML to make a nice looking chat bot
#   Use langchain framework to read .pdf files
#   Use an open source LLM that doesn't cost tokens

# pip install this dependency if you don't have this already
# pip install python-dotenv openai
# pip install --upgrade openai
# pip install --upgrade python-dotenv
import openai
from dotenv import load_dotenv
import os
from apikey import apikey

os.environ["OPENAI_API_KEY"] = apikey

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI library with your API key
openai.api_key = apikey

from openai import OpenAI

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

# User-defined function go here, before the main() function (is a Python coding convention)
def generate_response(user_input):
    try:

        messages = [
            {"role": "system",
             "content": "You are a wonderful assistant for aspiring chefs named Bella, and you help them find delicious recipes, suggest creative meal ideas, and guide them through cooking step-by-step. You are knowledgeable about various cuisines, dietary restrictions, and cooking techniques. Your goal is to make cooking enjoyable and accessible for everyone."},
            {"role": "assistant", "content": "Hello fellow chef! What is your name?"},
            {"role": "user", "content": "Hello. My name is Jack."},
            {"role": "user", "content": "Tell me a recipe."},
            {"role": "assistant", "content": "To make a quick and delicious garlic butter pasta, start by cooking 200g of spaghetti in salted boiling water according to the package instructions. Once cooked, drain the pasta and set it aside. In a large pan, melt 3 tablespoons of butter over medium heat, then add 3 minced garlic cloves and sauté them until fragrant, which should take about 1-2 minutes. Add the cooked spaghetti to the pan and toss it well to coat the noodles in the garlic butter. Season with salt and pepper to taste. For an extra touch, garnish with grated Parmesan cheese and freshly chopped parsley before serving. Enjoy your simple and flavorful meal! 🍝"},
            {"role": "user", "content": "Tell me more recipes."},
            {"role": "assistant", "content": "For a quick and tasty turkey stir-fry, start by slicing 200g of turkey breast into thin strips. Heat a tablespoon of olive oil in a large pan or wok over medium-high heat. Add the turkey strips and cook for about 5-7 minutes until browned and cooked through. Remove the turkey from the pan and set aside. In the same pan, add a bit more oil if needed, and sauté a chopped onion, 1 bell pepper, and 2 cloves of garlic for about 3-4 minutes, until softened. Then, add 2 tablespoons of soy sauce, 1 tablespoon of honey, and a pinch of black pepper to the vegetables, stirring to combine. Return the turkey to the pan, toss everything together, and cook for an additional 2 minutes until everything is well-coated and heated through. Serve your turkey stir-fry over rice or noodles, and enjoy a flavorful, healthy meal!"},
            {"role": "assistant", "content": "Quick Chicken Stir-Fry Ingredients: Chicken breast, bell pepper, soy sauce, garlic, olive oil. Instructions: Slice chicken and bell pepper. Sauté garlic in olive oil, add chicken and cook until browned. Add bell pepper and soy sauce, stir-fry for 5 minutes. Serve over rice."},
            {"role": "assistant", "content": "Simple Veggie Salad Ingredients: Lettuce, cherry tomatoes, cucumber, olive oil, lemon, salt. Instructions: Chop lettuce, tomatoes, and cucumber. Toss with olive oil, lemon juice, and a pinch of salt. Serve :)"},
            {"role": "user", "content": "What was your first recipe?"},
            {"role": "user", "content": "What was your second recipe?"},
            {"role": "user", "content": "What was your third recipe?"},
            {"role": "user", "content": "What was your fourth recipe?"}
        ]  # The chatbot only seems to remember the content under the first "assistant" key/value pair. There is a limit to the total memory that the chatbot can store.

        # Call the OpenAI API to generate a response
        messages.append({"role": "user", "content": user_input})
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages)
        print(completion.choices[0].message)

        # Extract the text of the response
        response_text = completion['choices'][0]['message']['content']
        return response_text

    except Exception as e:
        # Print an error message if the API call fails
        print("Error generating response:", e)
        return "I'm sorry, I couldn't generate a response."

def main():
    # This API key will not work (Because I deleted it after the video)
    # Use your own from OpenAI (there is a cost for this, but it is not much if you do not deploy
    # your app and have thousands of users) Typically, your API key will be in another Python file that
    # GitHub will not fork when asked to download
    # https://platform.openai.com/api-keys

    # Print a welcome message
    print("\nWelcome to the Recipe Suggester Chatbot! Type 'quit' to exit.\n")

    # This loop will run until the break after user input "quit"
    while True:
        # Get user input.
        user_input = input("Aspiring Chef Question: ")

        # Check if user wants to quit the chatbot
        if user_input.lower() == "quit":
            print("Exiting Recipe Suggester Bot.")
            break

        # Generate a response using OpenAI's GPT-3.5-turbo
        response = generate_response(user_input)

        # Print the response
        print("Recipe Suggester Bot:", response)

# Use this common Python idiom to check if your Python code is being run directly or being imported
# as a module into another program. This tells your program to start in a function named "main()"
# main() is not a reserved word in Python, but it is a standard convention and I suggest you use it
# to not confuse your project coworkers.
if __name__ == "__main__":
    main()
