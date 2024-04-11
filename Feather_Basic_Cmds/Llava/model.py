import os
import replicate
os.environ['REPLICATE_API_TOKEN'] = 'r8_73YZHxpxrTuhLYrAe8GcwvggpifC7BZ1QT7xB'

def analyze_speech(speech):
    print("Thinking...")
    input = {
        "image": open("rsc\droneFlightTest.jpg", "rb"),
        "prompt": f"""A chat between a human drone user and an extremely helpful and refined artificial intelligence assistant who writes code to control the drone to satisfy the human's requests. 
            The drone is equipped with a camera on the front.
            You are writing code to control a drone. You may use only the following commands:
            back(x) - Move the drone x centimeters backwards, where x is in the range of 20 to 200.
            down(x) - Move the drone x centimeters down, where x is in the range of 20 to 200.
            forward(x) - Move the drone x centimeters forward, where x is in the range of 20 to 200.
            left(x) - Move the drone x centimeters left, where x is in the range of 20 to 200.
            right(x) - Move the drone x centimeters right, where x is in the range of 20 to 200.
            up(x) - Move the drone x centimeters up, where x is in the range of 20 to 200.
            takeoff() - Takeoff the drone.
            land() - Land the drone.
            Return a combination of up to 5 of the above commands, separated onto new lines, without any extraneous code or comments, to execute the following actions.
            Write me between 1 and 5 lines of code to make the drone {speech}. You do not necessarily need to write exactly 5 lines of code, but you may if needed. Respond with code, separated by whitespaces.
            
            """
    }

    output = replicate.run(
        "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
        input=input
    )
    outputstr = "".join(output)
    #print(outputstr)

    commands = outputstr.splitlines(keepends=False)
    to_return = []

    for c in commands:
        if c == "takeoff()" or c == "land()":
            to_return.append(c)
        else:
            to_return.append("move_" + c)
    return to_return