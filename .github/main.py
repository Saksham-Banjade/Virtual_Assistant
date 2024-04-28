import openai
import gtts
import os
import pygame
import time

# Configuration
openai.api_key = 'your-api-key'
# Replace your-api-key with actual OpenAI API
gtts_lang = 'en'
gtts_slow = False
pygame.mixer.init()

# Function to generate a response from fetched input
def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I encountered an error."

# Function to convert text to speech
def text_to_speech(text, filename):
    try:
        tts = gtts.gTTS(text=text, lang=gtts_lang, slow=gtts_slow)
        tts.save(filename)
    except Exception as e:
        print(f"Error converting text to speech: {e}")

# Function to play audio file
def play_audio(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")

# Function to clean up temporary files
def cleanup_files(filenames):
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)

# Function to validate user input
def validate_input(user_input):
    if user_input.lower() == "quit":
        return False
    return True

# Main function
def main():
    filenames = []
    while True:
        user_input = input("You: ")
        if not validate_input(user_input):
            break
        response_text = generate_response(user_input)
        print("Bot: " + response_text)
        filename = "response.mp3"
        filenames.append(filename)
        text_to_speech(response_text, filename)
        play_audio(filename)
        time.sleep(1) # Wait for the audio to finish playing
    cleanup_files(filenames)

if __name__ == "__main__":
    main()
