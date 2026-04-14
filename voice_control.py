"""Module for handling voice commands and real-time blockchain transaction alerts."""
import speech_recognition as sr
import os
import subprocess

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Voice Command Engine Active. Listening for 'System'...")
        recognizer.adjust_for_ambient_noise(source)
        
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                
                if "system" in command:
                    print(f"Wake word detected. Processing: {command}")
                    
                    if "start listener" in command:
                        subprocess.Popen(["python3", "blockchain_listener.py"])
                        print("Blockchain listener initiated.")
                        
                    elif "stop bot" in command:
                        os.system("pkill -f bot.py")
                        print("Bot process terminated.")
                        
                    elif "lockdown" in command:
                        os.system("pkill -f python3")
                        print("Emergency Lockdown: All processes killed.")
                        break
            
            except sr.UnknownValueError:
                pass # Ignore background noise
            except sr.RequestError:
                print("Voice service unavailable.")

if __name__ == "__main__":
    listen_for_commands()
