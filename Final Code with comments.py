# Imports Tkinter which is used to create GUI.
# Imports Isec which is used to simulate the hardware for the lights.
# Imports Thread which is used to thread the automation of the program.
# Imports Time which is used to create a delay.
from Tkinter import* 
import isec 
import time
import thread
#This is an array used to identify which lights are on.
#The first indice is the current state of an intersection.
#The second indice is the specific light within the intersection.
STATE2 = [[1,0,0,1,0,0],
          [0,0,1,1,0,0], 
          [0,1,0,1,0,0],
          [1,0,0,1,0,0],
          [1,0,0,0,0,1], 
          [1,0,0,0,1,0]]
#This is the array that stores what the next state,
#of the Finite state machine is. Also called a state transition table.
#States are reassigned based on the current state, and 
#two sensor values. This is a 3d array. 
#is sensor in A direction, and 3rd indice is sensor in B direction.
#The first indice is current state, the second indice is
STATE = [[[1 , 1],[ 1, 1]], 
         [[ 1 , 2],[ 1, 2]], 
         [[ 3, 3], [ 3, 3]], 
         [[ 4, 4], [ 4, 4]], 
         [[ 4, 4], [ 5, 5]],
         [[ 0, 0], [ 0, 0]]]
#'LIGHT' is an array that stores the light labels.
#'color' is a dictionary used to pass a light label and return the color for that light when it
#is turned on, 'color2' is the same but for when the light is off. The colors are for the GUI.
LIGHT = ['AR','AY','AG','BR','BY','BG'] 
color = {'AR':'#FF0000','AY':'yellow','AG':'#00FF00','BR':'#FF0000','BY':'yellow','BG':'#00FF00'}
color2 = {'AR':'#8B0000','AY':'#A29C04','AG':'darkgreen','BR':'#8B0000','BY':'#A29C04','BG':'darkgreen'}
# this is the function used by the auto button.
# evaluates the for loop for all of the objects stored in OBJECTS array.
# a.go becomes 'the name of the object'.go
# a.go is a variable that determines if the auto is on or off for all 5 lights.
# This changes the label for the status of automation to off.
# When a.go is true automation is on, when false automation is off.
# Sets the label for automation status to on.
def Startauto(): 
    for a in OBJECTS:
        if a.go == True:  
            a.go = False 
            autovar.set('Auto is OFF')
            
        else:
            a.go = True
            autovar.set('Auto is ON for intersections with a Checkmark')
# Function for the Exit Button.
# deinitializes the Hardware.
#destroys the GUI window.
def exit():
    isec.hw_close()
    root.destroy() 	
# Starts the properties for a class which models an intersection in the GUI and hardware.
class INTERSECTION: 
#The next block of code executes when a class object is made as the initizalization.
#Sets up the GUI and the state varible for one intersection.
    def __init__(self, intersection,master): 
       self.int = intersection
       self.cs = 0 
       self.go = False
       self.frame = Frame(master) 
       self.frame.grid(row = 0,column = self.int)
       Label(self.frame, text=(self.int), font=('helvetica', 20, 'underline italic')).grid()
       Label(self.frame, text='A                      B', font = 50).grid()
       self.canvas = Canvas(self.frame, width=200, height=300, bg='white') 
       self.canvas.grid()
       self.AR= self.canvas.create_oval(5, 5, 95, 95, width=5, fill='purple') 
       self.AY= self.canvas.create_oval(5, 105, 95, 195, width=5, fill='purple') 
       self.AG= self.canvas.create_oval(5, 205, 95, 295, width=5, fill='purple') 
       self.BR= self.canvas.create_oval(105, 5, 195, 95, width=5, fill='purple')
       self.BY= self.canvas.create_oval(105, 105, 195, 195, width=5, fill='purple')
       self.BG= self.canvas.create_oval(105, 205, 195, 295, width=5, fill='purple')
       self.lightcan = [self.AR, self.AY, self.AG, self.BR, self.BY, self.BG]
       self.SensorA = StringVar()
       self.SensorB = StringVar()
       self.sensorA = Label(self.frame, textvariable= self.SensorA, fg = 'black', bg = 'yellow').grid()
       self.sensorB = Label(self.frame, textvariable= self.SensorB, fg = 'black', bg = 'yellow').grid()
       self.var = IntVar()
       self.chk = Checkbutton(self.frame, text=('Check for auto on ' + str(self.int)), variable=self.var)  
       self.chk.grid()
       Manual = Button(self.frame, text = ('Manual Change '+ str(self.int)), command = self.statecycle)
       Manual.grid()
#Function used for the automation as a thread object. 
#While loop that runs infinitely.
#While loop that runs when check button is checked and self.go is true.
#If statment to make sure extra sensor is checked on intersection 1.
#Previous line assicns next state based on current state and the status of the sensors.
#If not intersection 1 then only 3 sensors checked not 4.
#Calls the Change Light and Canvas Functions.
#Prints status of lights to console window.
#Uses sleep function in time to create 2 second delay.
    def auto(self): 
        while 1:
            chk = isec.sense
            while self.var.get() == 1 and self.go == True: 
                if self.int == 1: 
                    self.cs = STATE [self.cs] [(chk(self.int,'A1') or chk(self.int,'C1')) ] [chk(self.int,'B1') or chk(self.int,'D1')]   
                else:      
                    self.cs = STATE [self.cs] [(chk(self.int,'A1') or chk(self.int,'C1')) ] [chk(self.int,'B1')]
                self.chlt()
                self.chcv()
                self.chksens()
                time.sleep(2)
            self.chksens()
            time.sleep(.7)
#Function Created to check sensors and update a label indicating
#the presence of a car so GUI can be used without needing to see
#the intersections.
    def chksens(self):
        if isec.sense(self.int,'A1')==True or isec.sense(self.int, 'C1') ==True:
            self.SensorA.set('Car Waiting In A Direction')
        else:
            self.SensorA.set('No Car')
        if self.int == 1:
            if isec.sense(self.int,'B1')==True:
                self.SensorB.set('Car Waiting In B Direction')
        if isec.sense(self.int,'B1')==True:
            self.SensorB.set('Car Waiting In B Direction')
        else:
            self.SensorB.set('No Car')
#For loop evaluates 'light' as each of the labels stored in LIGHT array.
#Enumerate makes the varible become the indice of the for loop is on
#for the LIGHT array, which corresponds to the indice location
#in the STATE2 array for each light in the intersection. 
#References the STATE2 array to determine the if light is on or off in the current state.
#This turns the light on in the hardware.
#Turns light off in the hardware.  
    def chlt(self):        
        for (e,light) in enumerate(LIGHT):
            if STATE2 [self.cs] [e] == 1:
                isec.light_on(self.int, light)
            else:
                isec.light_off(self.int, light)
#For loop that evaluates 'light3' as each stored oval in 'self.lightcan', and
#enumerate allows the varible e to be replaced with the 
#indice location of the current oval within the array 'self.lightcan'
#Checks the status of the individual light within the intersection.   
#Reconfigures the oval within the GUI to mirror the status of the light in the intersection.
#The ovals are dark when off and bright when on.
    def chcv(self):
        for (e,light3) in enumerate(self.lightcan):
            if isec.light_status((self.int),LIGHT[e]):
                self.canvas.itemconfig(light3, fill = color[LIGHT[e]])
            else:
                self.canvas.itemconfig(light3, fill = color2[LIGHT[e]])
#Function used to manually control lights.
#During automation state is assigned based on sensors, in manual it assumes sensors are always true.
#Following block of code is same as in the auto function.
    def statecycle(self):     
        self.cs = STATE [self.cs] [1] [1]
        self.chlt()
        self.chcv()
        self.chksens()
        isec.print_lights()
#isec.hw_init(simulate_hardware = False, use_one_intersection = False)
# Creates the main window, initializes the isec, creates the
#intersection objects, Makes an array of the objects.
#Creates 5 threads that run the auto functions for each intersection object.
#Creates a button for the automation, exit, and makes the auto label.
root = Tk()
root.title ('Light Control System')
root.geometry ('1100x500')
isec.hw_init()
isec.simulate_hardware = True 
isec.sensor_value_from_user = False 
HI1 = INTERSECTION(1,root)
HI2 = INTERSECTION(2,root)
HI3 = INTERSECTION(3,root)
HI4 = INTERSECTION(4,root)
HI5 = INTERSECTION(5,root)
OBJECTS = [HI1,HI2,HI3,HI4,HI5]
thread.start_new(HI1.auto, ())
thread.start_new(HI2.auto, ())
thread.start_new(HI3.auto, ())
thread.start_new(HI4.auto, ())
thread.start_new(HI5.auto, ())
Button(text = ('Auto On/Off'), command = Startauto).grid(row = 1, column=3)
Button(text = ('Exit'), width = '10', command = exit, bg = 'red',font=('helvetica', 15, 'underline italic')).grid(row = 3, column=3)
autovar = StringVar()
autodisplay = Label(root, textvariable= autovar, fg = 'White', bg = 'black').grid(row=1,column=4)
autovar.set('Auto is OFF')
root.mainloop()
