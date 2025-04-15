from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import time
import os
import sys

# Load environment variables from .env file
load_dotenv()

# Check if API key exists
api_key = os.getenv('OPENAI_API_KEY')
if not api_key or api_key == "your-api-key-here":
    print(" Error: OPENAI_API_KEY not found in .env file or invalid!")
    print("Please add your OpenAI API key to the .env file.")
    sys.exit(1)

# Initialize OpenAI client with API key
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f" Error initializing OpenAI client: {str(e)}")
    sys.exit(1)

def get_voice_selection():
    voices = {
        '1': 'alloy',    # Default balanced voice
        '2': 'echo',     # Warm and friendly voice
        '3': 'fable',    # British accent, authoritative
        '4': 'onyx',     # Deep and powerful voice
        '5': 'nova',     # Energetic and bright voice
        '6': 'shimmer'   # Clear and expressive voice
    }
    
    print("\n=== Available Voices ===")
    for key, voice in voices.items():
        print(f"{key}. {voice}")
    
    while True:
        choice = input("\nSelect a voice (1-6): ")
        if choice in voices:
            return voices[choice]
        print("❌ Invalid choice. Please select a number between 1 and 6.")

def create_speech(text, voice, filename):
    speech_file_path = Path(__file__).parent / filename
    
    try:
        print(f"\nGenerating speech using {voice} voice...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        with open(speech_file_path, "wb") as f:
            f.write(response.content)
        
        print(f"✨ Audio saved to {speech_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating speech: {str(e)}")
        return False

def play_audio(filename):
    try:
        if os.name == 'posix':  # macOS or Linux
            if sys.platform == 'darwin':  # macOS
                os.system(f"afplay {filename}")
            else:  # Linux
                os.system(f"play {filename}")
        else:
            print("Note: Auto-playback is not supported on Windows.")
    except Exception as e:
        print(f"❌ Error playing audio: {str(e)}")

def main():
    print("🎤 Welcome to Enhanced Text-to-Speech Generator! 🎤")
    
    while True:
        print("\n=== Menu ===")
        print("1. Generate new speech")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '2':
            print("\nThank you for using the Text-to-Speech Generator! Goodbye! 👋")
            break
        
        if choice == '1':
            # Get text input
            while True:
                text = input("\nEnter the text you want to convert to speech: ").strip()
                if text:
                    break
                print("❌ Text cannot be empty. Please try again.")
            
            # Get voice selection
            voice = get_voice_selection()
            
            # Generate unique filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"speech_{timestamp}.mp3"
            
            # Create the speech
            if create_speech(text, voice, filename):
                # Ask if user wants to play the audio
                if os.name != 'nt':  # Not Windows
                    play = input("\nWould you like to play the audio? (y/n): ")
                    if play.lower() == 'y':
                        play_audio(filename)
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()