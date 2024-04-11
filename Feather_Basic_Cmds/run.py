from Vosk import speech_recog as sr
from Llava import model as llava_model

def run_program():
    print("Listening...")
    while True: 
        try:
            speech = sr.listen()
        except:
            print("I'm sorry. I don't understand")
            run_program()
        else:
            if speech != "" and speech != "exit":
                print(speech)
                commands = []
                commands = llava_model.analyze_speech(speech)
                for c in commands:
                    print(c)
                print("Listening...")
            if speech == "exit":
                print(speech)
                print("Exiting the program")
                exit()

if  __name__ == '__main__':
    run_program()