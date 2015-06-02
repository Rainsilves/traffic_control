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
STATE = [[[1 , 1],[ 1, 1]], 
         [[ 1 , 2],[ 1, 2]], 
         [[ 3, 3], [ 3, 3]], 
         [[ 4, 4], [ 4, 4]], 
         [[ 4, 4], [ 5, 5]],
         [[ 0, 0], [ 0, 0]]]
LIGHT = ['AR','AY','AG','BR','BY','BG'] 
color = {'AR':'#FF0000','AY':'yellow','AG':'#00FF00','BR':'#FF0000','BY':'yellow','BG':'#00FF00'}
color2 = {'AR':'#8B0000','AY':'#A29C04','AG':'darkgreen','BR':'#8B0000','BY':'#A29C04','BG':'darkgreen'}
def Startauto(): 
    for a in OBJECTS:
        if a.go == True:  
            a.go = False 
            autovar.set('Auto is OFF')
            
        else:
            a.go = True
            autovar.set('Auto is ON for intersections with a Checkmark')
def exit():
    isec.hw_close()
    root.destroy() 	
class INTERSECTION: 
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
    def chlt(self):        
        for (e,light) in enumerate(LIGHT):
            if STATE2 [self.cs] [e] == 1:
                isec.light_on(self.int, light)
            else:
                isec.light_off(self.int, light)
    def chcv(self):
        for (e,light3) in enumerate(self.lightcan):
            if isec.light_status((self.int),LIGHT[e]):
                self.canvas.itemconfig(light3, fill = color[LIGHT[e]])
            else:
                self.canvas.itemconfig(light3, fill = color2[LIGHT[e]])
    def statecycle(self):     
        self.cs = STATE [self.cs] [1] [1]
        self.chlt()
        self.chcv()
        self.chksens()
        isec.print_lights()
root = Tk()
root.title ('Light Control System')
root.geometry ('1100x530')
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
