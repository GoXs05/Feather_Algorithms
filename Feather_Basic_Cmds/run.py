from Vosk import speech_recog as sr
from Llava import model as llava_model

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='basic controls')
    parser.add_argument('-use_speech', default=False, action='store_const', const=True, help='Use speech recognition or not?')

    args = parser.parse_args()
    return args

def run_voice_program():
    print("Please tell me what you want your drone to do!")
    print("Listening...")
    speech = sr.listen()
    if speech != "" and speech != "exit":
        print(speech)
        commands = []
        commands = llava_model.analyze_speech(speech)
        for c in commands:
            print(c)
    if speech == "exit":
        print("Exiting the program!")
        exit()

def run_text_program():
    speech = input('Please enter what you want your drone to do:\n')
    if speech != "" and speech != "exit":
        commands = []
        commands = llava_model.analyze_speech(speech)
        for c in commands:
            print(c)
    if speech == "exit":
        print("Exiting the program!")
        exit()


if  __name__ == '__main__':
    args = parse_args()
    print(args.use_speech)

    while True:
        if args.use_speech:
            run_voice_program()
        else:
            run_text_program()