import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
import pyttsx3  # For text-to-speech

# Set the OpenAI API key directly in the code
openai.api_key = "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"  # Replace with your OpenAI API key

# Global chat history for conversation with AI
chatStr = ""

# Function to chat with the AI and get responses
def chat(query):
    global chatStr  # Ensure global declaration is here
    print(chatStr)
    chatStr += f"Harry: {query}\n Jarvis: "
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
        print(f"Error interacting with OpenAI API: {e}")
        return "Sorry, I couldn't process your request right now."

# Function to process AI prompts and save responses to a file
def ai(prompt):
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"]

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Openai/{timestamp}_{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        
        with open(filename, "w") as f:
            f.write(text)
        print(f"Response saved to {filename}")
    except Exception as e:
        print(f"Error processing AI prompt: {e}")

# Function to use text-to-speech to say something
def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135.0)  # Set speech rate (default ~200)
    engine.setProperty('volume', 0.9)  # Set volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# Function to listen to user command via speech recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return "Sorry, I did not catch that."
        except sr.RequestError:
            print("Service is unavailable.")
            return "Sorry, I am unable to reach the service right now."
        except Exception as e:
            print(f"Error with speech recognition: {e}")
            return "Sorry, something went wrong."

# Function to handle website opening based on user input
def openWebsite(query):
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["facebook", "https://www.facebook.com"],
        ["instagram", "https://www.instagram.com"],
        ["twitter", "https://www.twitter.com"],
        ["reddit", "https://www.reddit.com"],
        ["discord", "https://www.discord.com"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://www.stackoverflow.com"],
        
    ]
    
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])

# Main loop to run the assistant
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I is online.")
    
    while True:
        query = takeCommand().lower()
        
        # Handle website opening
        openWebsite(query)
        
        # Handle music playing
        if "open video" in query:
            videoPath = "/home/rudddyy/Downloads/Wallpaper/orange-train-at-sunset.3840x2160.mp4"  # Update the path as needed
            try:
                os.system(f"xdg-open '{videoPath}'")
                say("Opening video.")
            except Exception as e:
                print(f"Error opening Video: {e}")
                say("Sorry, I couldn't open the video.")
        
        # Tell the current time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")
            
        # AI interaction
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Quit Jarvis
        elif "jarvis quit" in query:
            say("Goodbye, sir.")
            break

        # Reset chat history
        elif "reset chat" in query:
            #global chatStr  # Declare global before assignment
            chatStr = ""  # Reset the global chatStr variable
            say("Chat history reset.")
        
        # General AI chat
        else:
            chat(query)
