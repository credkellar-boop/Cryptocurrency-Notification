
"""Module for handling voice commands and system lockdown."""
import os
import subprocess
import speech_recognition as sr

def listen_for_commands():
    """Listens for 'System' wake word and executes commands."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Voice Engine Active. Listening for 'System'...")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio).lower()

                if "system" in text:
                    print(f"Command Detected: {text}")

                    if "activate" in text:
                        subprocess.Popen(["python3", "blockchain_listener.py"])
                        print(">> Blockchain Listener Started.")

                    elif "lockdown" in text:
                        os.system("pkill -f blockchain_listener.py")
                        os.system("pkill -f bot.py")
                        print(">> EMERGENCY LOCKDOWN: All processes killed.")
                        break

            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue
            except sr.RequestError:
                print("Voice service unavailable.")
                break

if __name__ == "__main__":
    listen_for_commands()
