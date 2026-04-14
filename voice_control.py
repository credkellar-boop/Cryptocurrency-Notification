
"""Module for handling voice commands and emergency protocols"""
import os
import subprocess
import speech_recognition as sr

def listen_for_commands():
    """Listens for 'System' wake word and executes blockchain protocols"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Voice Engine Active. Listening for 'System'...")
        # Adjust for ambient noise to improve accuracy in different rooms
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                # Listen for audio input
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                # Convert speech to text using Google's engine
                text = recognizer.recognize_google(audio).lower()

                if "system" in text:
                    print(f"Command Detected: {text}")

                    # Logic to start the monitoring bot
                    if "activate" in text:
                        print(">> Activating Cryptocurrency-Notification Hub...")
                        subprocess.Popen(["python3", "main.py"])
                    
                    # Logic for Emergency Lockdown (Insert 3)
                    elif "lockdown" in text or "emergency" in text:
                        print(">> EMERGENCY PROTOCOL INITIATED")
                        # Terminate the main monitoring process immediately
                        os.system("pkill -f main.py")
                        # Trigger the security wipe to clear cached session data
                        subprocess.Popen(["python3", "security_wipe.py"])
                        print(">> System Secure. Monitoring Halted.")

            except sr.UnknownValueError:
                # Occurs when the engine can't decipher the audio
                continue 
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service; {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    listen_for_commands()
