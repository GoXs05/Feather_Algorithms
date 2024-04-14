from djitellopy import tello

def connect(dr1):
    dr1.connect()
    print(dr1.get_battery())
    print(dr1.get_height())

def format_cmds(cmds):
    cmd_run = []
    for i in range(len(cmds)):
        cmd_run.append("dr1." + cmds[i])
    return cmd_run

def execute(cmds, dr1):
    if cmds[0] != "dr1.takeoff()":
        if dr1.get_height() == 0:
            cmds.insert(0, "dr1.takeoff()")
    for i in cmds:
        try:
            exec(i)
        except tello.TelloException as Argument:
            print(str(Argument))