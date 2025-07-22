import speech_recognition as sr

def main():
      r = sr.Recognizer()
      with sr.Microphonne() as source:
            r.adjust_for_ambient_noise(source)# ye hamrare background noice kko reduse karega 

