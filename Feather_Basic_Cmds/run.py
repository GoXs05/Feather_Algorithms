from Vosk import speech_recog as sr
from Llava import model as llava_model
from TelloRun import drone_movement as drone_ctrls
from djitellopy import tello

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='basic controls')
    parser.add_argument('-use_speech', default=False, action='store_const', const=True, help='Use speech recognition or not?')

    args = parser.parse_args()
    return args

def run_voice_program(dr1):
    print("Please tell me what you want your drone to do!")
    print("Listening...")
    speech = sr.listen()
    if speech != "" and speech != "exit":
        print(speech)
        commands = []
        commands = llava_model.analyze_speech(speech)
        cmds = drone_ctrls.format_cmds(commands)
        for c in cmds:
            print(c)
        drone_ctrls.execute(cmds, dr1)
    if speech == "exit":
        print("Exiting the program!")
        exit()

def run_text_program(dr1):
    speech = input('Please enter what you want your drone to do:\n')
    if speech != "" and speech != "exit":
        commands = []
        commands = llava_model.analyze_speech(speech)
        cmds = drone_ctrls.format_cmds(commands)
        for c in cmds:
            print(c)
        drone_ctrls.execute(cmds, dr1)
    if speech == "exit":
        print("Exiting the program!")
        exit()


if  __name__ == '__main__':
    args = parse_args()
    print(args.use_speech)

    dr1 = tello.Tello()
    drone_ctrls.connect(dr1)

    while True:
        if args.use_speech:
            run_voice_program(dr1)
        else:
            run_text_program(dr1)