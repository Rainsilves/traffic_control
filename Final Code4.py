from Tkinter import*
import isec
import time
import thread
STATE2 = [[1,0,0,1,0,0],
          [0,0,1,1,0,0],
          [0,1,0,1,0,0],
          [1,0,0,1,0,0],
          [1,0,0,0,0,1],
          [1,0,0,0,1,0]]
STATE = [[[1 , 1],[ 1, 1]], #This is the array
         [[ 1 , 2],[ 1, 2]], #That controls the state, of the Finite state machine
         [[ 3, 3], [ 3, 3]], #States are reassgned based on the current state, and 
         [[ 4, 4], [ 4, 4]], #two sensor values.
         [[ 4, 4], [ 5, 5]], #This is a 3d array.
         [[ 0, 0], [ 0, 0]]] #		 
LIGHT = ['AR','AY','AG','BR','BY','BG']
OVALS1 = {'AR':0,'AY':0,'AG':0,'BR':2,'BY':2,'BG':2}
OVALS2 = {'AR':1,'AY':1,'AG':1,'BR':3,'BY':3,'BG':3}
color = {'AR':'#FF0000','AY':'yellow','AG':'#00FF00','BR':'#FF0000','BY':'yellow','BG':'#00FF00'}
color2 = {'AR':'black','AY':'black','AG':'black','BR':'black','BY':'black','BG':'black'}
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
    def __init__(self, master,row,column,intersection,):
       self.row = row
       self.column = column
       self.intersection = intersection
       self.cs = 0
       self.go = False
       self.frame = Frame(master)
       self.frame.grid(row = self.row,column = self.column)
       self.canvas = Canvas(self.frame, width= 99, height= 99, bg='white')
       self.canvas.grid(row = 2)
       self.A1= self.canvas.create_oval(1, 33, 33, 66, width=1, fill='pink')
       self.B1= self.canvas.create_oval(33, 1, 66, 33, width=1, fill='pink')
       self.A2= self.canvas.create_oval(66, 33, 99, 66, width=1, fill='pink')
       self.B2= self.canvas.create_oval(33, 66, 66, 99, width=1, fill='pink')
       Label(self.frame, text=(self.intersection), font=('helvetica', 20, 'underline italic')).grid(row=0,column=0)
       Button(self.frame, text = ('Change Intersection '+ str(self.intersection) + ' Manual'), command = self.statecycle).grid(row = 4, column=0)
       self.lightcan = [self.A1, self.A2, self.B1, self.B2]
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
                #isec.print_lights()
                time.sleep(2)
            time.sleep(2)
            print('Auto off for' + str(self.intersection))
    def chlt(self):        
        for (e,light) in enumerate(LIGHT):
            if STATE2 [self.cs] [e] == 1:
                isec.light_on(self.intersection, light)
            else:
                isec.light_off(self.intersection, light)
    def chcv(self):
        for light in LIGHT:
            if isec.light_status((self.intersection),light):
                self.canvas.itemconfig(self.lightcan[OVALS1[light]], fill = color[light])
                self.canvas.itemconfig(self.lightcan[OVALS2[light]], fill = color[light])
    def statecycle(self):         
        self.cs = STATE [self.cs] [1] [1]
        self.chlt()
        self.chcv()

#isec.hw_init(simulate_hardware = False, use_one_intersection = False) # Initializes the software.
root = Tk()
root.title ('Light Control System')
root.geometry ('750x700')
isec.hw_init()
isec.simulate_hardware = True #Turns on simulation software.
isec.sensor_value_from_user = False #Allows user to enter sensor data.
HI1 = Lights(root,3,3,1)
HI2 = Lights(root,1,3,2)
HI3 = Lights(root,3,5,3)
HI4 = Lights(root,5,3,4)
HI5 = Lights(root,3,1,5)
OBJECTS = [HI1,HI2,HI3,HI4,HI5]
thread.start_new(HI1.statecycle2, ())
thread.start_new(HI2.statecycle2, ())
thread.start_new(HI3.statecycle2, ())
thread.start_new(HI4.statecycle2, ())
thread.start_new(HI5.statecycle2, ())
Button(text = ('Auto On/Off'), command = Startauto).grid(row = 6, column=3)
Button(text = ('Exit'), width = '10', command = exit, bg = 'red',font=('helvetica', 15, 'underline italic')).grid(row = 7, column=3)
autovar = StringVar()
autodisplay = Label(root, textvariable= autovar, fg = 'White', bg = 'black').grid(row=6,column=5)
autovar.set('Auto is OFF')
root.mainloop()
isec.hw_close()
