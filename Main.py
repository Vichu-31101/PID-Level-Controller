#!/bin/python3

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plot
import time
from random import randint

# Global Variables
processVariable = 0
setPoint = 0
x = np.linspace(0, 100, 201)
y = np.zeros(201)
iteration = 0


# Plant
def Plant(plantInput):
    k = 7
    p = 5
    f = 5
    # Plant function
    output = (k * plantInput / p) - f
    return output


# P controller class
class pController:
    Kp = 0

    def output(self, error):
        return self.Kp * error


# I controller class
class iController:
    # Integrating Error
    errorI = 0
    Ki = 0

    def output(self, error):
        self.errorI += error
        return self.Ki * self.errorI


# D controller class
class dController:
    # Differentiating Error
    errorD = 0
    prevError = 0
    Kd = 0

    def output(self, error):
        self.errorD = error - self.prevError
        self.prevError = error
        return self.Kd * self.errorD


# P control
pControl = pController()
# Gain value of P controller
pController.Kp = 0.62

# I control
iControl = iController()
# Gain value of I controller
iControl.Ki = 0.085

# D control
dControl = dController()
# Gain value of D controller
dControl.Kd = 0.045


# Control Loop
def controller():
    global processVariable
    global setPoint
    global x
    global y
    global iteration
    currentLevel.config(text="Current Level: " + str(processVariable))
    error = setPoint - processVariable
    # GUI
    if abs(error) < 1:
        s.configure("bar.Vertical.TProgressbar", background='orange')
        if abs(error) < 0.1:
            s.configure("bar.Vertical.TProgressbar", background='green')
            if abs(error) < 0.0001:
                setPointIndicator.configure(text="Set Point reached")
            else:
                setPointIndicator.configure(text="Set Point not reached")
    level.configure(style="bar.Vertical.TProgressbar", value=processVariable)
    # Calc. controller outputs
    pOutput = pControl.output(error)
    iOutput = iControl.output(error)
    dOutput = dControl.output(error)
    # Calc. plant input
    plantInput = pOutput + iOutput + dOutput
    # Clamping input value
    plantInput = min(100, plantInput)
    plantInput = max(0, plantInput)
    processVariable += Plant(plantInput)
    # Clamping level value
    processVariable = min(100, processVariable)
    processVariable = max(0, processVariable)
    print(error, processVariable)
    if iteration < 200:
        root.after(50, controller)
        y[1 + iteration] = processVariable
        iteration += 1
    else:
        # Plotting graph
        plot.plot(x, y)
        plot.plot(x, setPoint * np.ones(len(y)))
        plot.show()


# Initial parameters setting
def startController():
    global processVariable
    global setPoint
    global x
    global y
    global iteration
    setPoint = scale.get()
    processVariable = level['value']
    iControl.errorI = 0
    dControl.prevError = setPoint - processVariable
    label.config(text="Set Point: " + str(scale.get()))
    s.configure("bar.Vertical.TProgressbar", background='red')
    y[0] = processVariable
    iteration = 0
    controller()


# Update according to slider value
def setLabel(self):
    label.config(text="Set Point: " + str(scale.get()))


# Tkinter GUI
root = tk.Tk()
root.geometry("500x300")
scale = ttk.Scale(root, from_=0, to=100, command=setLabel)
button = ttk.Button(root, text="Start PID", command=startController)
s = ttk.Style()
s.theme_use('classic')
s.configure("bar.Vertical.TProgressbar", background='red')
level = ttk.Progressbar(root, style="bar.Vertical.TProgressbar", orient="vertical", length=300, mode="determinate")
label = ttk.Label(root, text="Set Point: 0")
currentLevel = ttk.Label(root, text="Process Variable: 0")
setPointIndicator = ttk.Label(root, text="Set Point not reached")
# Layout
level.pack(padx=20, pady=40, side=tk.LEFT)
button.pack(padx=50, pady=60, fill=tk.X, side=tk.BOTTOM)
scale.pack(padx=50, fill=tk.X, side=tk.BOTTOM)
label.pack(padx=50, fill=tk.X, side=tk.BOTTOM)
currentLevel.pack(padx=50, fill=tk.X, side=tk.BOTTOM)
setPointIndicator.pack(padx=50, fill=tk.X, side=tk.BOTTOM)
root.mainloop()
