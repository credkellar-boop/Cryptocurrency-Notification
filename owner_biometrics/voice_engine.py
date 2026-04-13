import speech_recognition as sr
import subprocess
import os
import time

def listen_for_system_commands():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("Voice Engine Active. Listening for 'System' wake word...")

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                audio = r.listen(source, timeout=None)
                text = r.recognize_google(audio).lower()
                
                if "system" in text:
                    print(f"Command Detected: {text}")
                    
                    if "activate listener" in text:
                        subprocess.Popen(["python3", "blockchain_listener.py"])
                        print(">> Blockchain Listener Online.")
                        
                    elif "bot status" in text:
                        # Logic to trigger a status update in your Telegram/Dashboard
                        print(">> Querying HFT Node Status...")
                        
                    elif "lockdown" in text:
                        print(">> EMERGENCY LOCKDOWN INITIATED.")
                        os.system("pkill -f python3")
                        break
            except sr.UnknownValueError:
                continue # Ignore background noise
            except Exception as e:
                print(f"Voice Engine Error: {e}")
                time.sleep(2)

if __name__ == "__main__":
