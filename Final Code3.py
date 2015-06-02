from Tkinter import*
import isec
import time
import thread
STATE2 = [[1,0,0,1,0,0],[0,0,1,1,0,0],[0,1,0,1,0,0],[1,0,0,1,0,0],[1,0,0,0,0,1],[1,0,0,0,1,0]]
STATE = [[[1 , 1],[ 1, 1]], #This is the array
         [[ 1 , 2],[ 1, 2]], #That controls the state, of the Finite state machine
         [[ 3, 3], [ 3, 3]], #States are reassgned based on the current state, and 
         [[ 4, 4], [ 4, 4]], #two sensor values.
         [[ 4, 4], [ 5, 5]], #This is a 3d array.
         [[ 0, 0], [ 0, 0]]] #		 
LIGHT = ['AR','AY','AG','BR','BY','BG']
color = {'AR':'#FF0000','AY':'yellow','AG':'#00FF00','BR':'#FF0000','BY':'yellow','BG':'#00FF00'}
color2 = {'AR':'#8B0000','AY':'#A29C04','AG':'darkgreen','BR':'#8B0000','BY':'#A29C04','BG':'darkgreen'}
def Startauto():
    for a in OBJECTS:
        if a.go == (True or 'stop'):
            a.go = False
            autovar.set('Auto is OFF')
            
        else:
            a.go = True
            autovar.set('Auto is ON for intersections with a Checkmark')
def signs():
    for a in OBJECTS:
        a.go = 'stop'
        autovar.set('Stop Signs')
    
def exit():
    root.destroy()
    isec.hw_close()
	
class Lights:
    def __init__(self, intersection,master):
       self.intersection = intersection
       self.cs = 0
       self.go = False
       self.frame = Frame(master)
       self.frame.grid(row = 0,column = self.intersection)
       self.canvas = Canvas(self.frame, width=200, height=300, bg='white')
       self.canvas.grid(row = 2)
       self.AR= self.canvas.create_oval(5, 5, 95, 95, width=5, fill='red')
       self.AY= self.canvas.create_oval(5, 105, 95, 195, width=5, fill='white')
       self.AG= self.canvas.create_oval(5, 205, 95, 295, width=5, fill='white')
       self.BR= self.canvas.create_oval(105, 5, 195, 95, width=5, fill='white')
       self.BY= self.canvas.create_oval(105, 105, 195, 195, width=5, fill='yellow')
       self.BG= self.canvas.create_oval(105, 205, 195, 295, width=5, fill='white')
       Label(self.frame, text=(self.intersection), font=('helvetica', 20, 'underline italic')).grid(row=0,column=0)
       Label(self.frame, text='A                      B', font = 50).grid(row=1,column=0)
       Button(self.frame, text = ('Change Intersection '+ str(self.intersection) + ' Manual'), command = self.statecycle).grid(row = 4, column=0)
       self.lightcan = [self.AR, self.AY, self.AG, self.BR, self.BY, self.BG]
       self.var = IntVar()
       self.chk = Checkbutton(self.frame, text=('Check box for auto on intersection ' + str(self.intersection)), variable=self.var)
       self.chk.grid()
       
    def statecycle2(self):
        while 1:
            while (self.var.get() == 1 and self.go == True):
                if self.intersection == 1:
                    self.cs = STATE [self.cs] [(isec.sense(self.intersection,'A1') or isec.sense(self.intersection,'C1')) ] [isec.sense(self.intersection,'B1') or isec.sense(self.intersection,'D1')]
                else:       
                    self.cs = STATE [self.cs] [(isec.sense(self.intersection,'A1') or isec.sense(self.intersection,'C1')) ] [isec.sense(self.intersection,'B1')]
                self.chlt()
                self.chcv()
                isec.print_lights()
                time.sleep(2)
            while (self.var.get() == 1 and self.go == 'stop'):
                for light in LIGHT:
                    isec.light_off(self.intersection, light)
                self.chcv()
                time.sleep(0.5)
                self.cs = 0
                self.chlt()
                self.chcv()
                time.sleep(0.5)
                
                     
    def chlt(self):        
        for (e,light) in enumerate(LIGHT):
            if STATE2 [self.cs] [e] == 1:
                isec.light_on(self.intersection, light)
            else:
                isec.light_off(self.intersection, light)
    def chcv(self):
        for (e,light3) in enumerate(self.lightcan):
            if isec.light_status((self.intersection),LIGHT[e]):
                self.canvas.itemconfig(light3, fill = color[LIGHT[e]])
            else:
                self.canvas.itemconfig(light3, fill = color2[LIGHT[e]])

    def statecycle(self):         
        self.cs = STATE [self.cs] [1] [1]
        self.chlt()
        self.chcv()
        isec.print_lights()

#isec.hw_init(simulate_hardware = False, use_one_intersection = False) # Initializes the software.
root = Tk()
root.title ('Light Control System')
root.geometry ('1100x500')
isec.hw_init()
isec.simulate_hardware = True #Turns on simulation software.
isec.sensor_value_from_user = False #Allows user to enter sensor data.
HI1 = Lights(1,root)
HI2 = Lights(2,root)
HI3 = Lights(3,root)
HI4 = Lights(4,root)
HI5 = Lights(5,root)
OBJECTS = [HI1,HI2,HI3,HI4,HI5]
thread.start_new(HI1.statecycle2, ())
thread.start_new(HI2.statecycle2, ())
thread.start_new(HI3.statecycle2, ())
thread.start_new(HI4.statecycle2, ())
thread.start_new(HI5.statecycle2, ())
Button(text = ('Auto On/Off'), command = Startauto).grid(row = 1, column=3)
Button(text = ('Exit'), width = '10', command = exit, bg = 'red',font=('helvetica', 15, 'underline italic')).grid(row = 3, column=3)
Button(text = ('Stop Signs'), command = signs).grid(row = 2, column=3)
autovar = StringVar()
autodisplay = Label(root, textvariable= autovar, fg = 'White', bg = 'black').grid(row=1,column=4)
autovar.set('Auto is OFF')
root.mainloop()
isec.hw_close()
