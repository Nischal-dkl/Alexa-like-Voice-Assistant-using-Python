import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from config import NEWS_API_KEY  # Import the API key from config.py

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def setting_up_voice():
    # Set voice to a more natural one (e.g., Microsoft Zira on Windows)
    for voice in voices:
        if 'Zira' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)  # Adjust speech rate if needed

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_website(url):
    webbrowser.open(url)

def play_music(song_name):
    song_name = song_name.lower()
    print(f"Looking for: {song_name}")  # Debugging line
    if song_name in musicLibrary.music:
        webbrowser.open(musicLibrary.music[song_name])
    else:
        speak(f"Sorry, I couldn't find {song_name} in the library.")
        print(f"Available songs: {list(musicLibrary.music.keys())}")  # Debugging line


def process_command(command):
    if "open google" in command:
        open_website("https://google.com")
    elif "open facebook" in command:
        open_website("https://facebook.com")
    elif "open youtube" in command:
        open_website("https://youtube.com")
    elif "open linkedin" in command:
        open_website("https://linkedin.com")
    elif "open instagram" in command:
        open_website("https://instagram.com")
    elif command.startswith("play"):
        play_music(command.split("play", 1)[1].strip())
        
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}")  # Use the imported API key
        
        # Check if the request was successful
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the headlines
            headlines = [article['title'] for article in data['articles']]
            
            # Display the headlines
            speak("Top Headlines:")
            for i, headline in enumerate(headlines, 1):
                speak(f"{i}. {headline}")
        else:
            speak(f"Failed to fetch headlines. Status code: {r.status_code}")

if __name__ == "__main__":
    setting_up_voice()
    speak("Initializing Alexa....")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = recognizer.listen(source, timeout=5)
                
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            
            if "alexa" in command:
                speak("Yes, how can I help you?")
                
                with sr.Microphone() as source:
                    print("Listening for command....")
                    audio = recognizer.listen(source)
                    
                user_command = recognizer.recognize_google(audio).lower()
                print(f"User's command: {user_command}")
                process_command(user_command)
        
        except sr.UnknownValueError:
            continue  # Ignore if speech is not understood
        except sr.RequestError as e:
            print(f"Error: {e}")
            continue  # Handle Google API request errors
        except Exception as e:
            print(f"Error: {e}")
            continue  # Handle other exceptions gracefully
