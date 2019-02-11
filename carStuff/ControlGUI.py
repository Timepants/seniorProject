import time
from MotorControl import MotorContol as Motor
from Tkinter import *

MC = Motor()

def key(event, e):
    inChar = repr(event.char)
    if 'w' in inChar:
        MC.setThrottle(int(e.get("1.0",'end-1c')))
        MC.sendCommand(MC.FORWARD)
    if 's' in inChar:
        MC.setThrottle(int(e.get("1.0",'end-1c')))
        MC.sendCommand(MC.BACKWARD)
    if 'q' in inChar:
        MC.sendCommand(MC.CLEAR_ALL)
    if 'e' in inChar:
        MC.sendCommand(MC.CLEAR_MOVEMENT)
    if '1' in inChar:
        MC.sendCommand(MC.CLEAR_HEADING)
    if 'a' in inChar:
        MC.sendCommand(MC.LEFT)
    if 'd' in inChar:
        MC.sendCommand(MC.RIGHT)
    MC.printSerial()

def main():
    print("Connecting to Arduino")
    
    

    root = Tk()
    isMoving = False
    isMovingForward = False
    frame = Text(root, width=10, height=1)
    e = Text(root, width=5, height=1)
    frame.bind("<Key>", lambda event, arg=e: key(event, arg))
    frame.pack()
    e.pack()
    frame.focus_set()
    root.mainloop()

    

if  __name__ =='__main__':
    main()
