from Tkinter import*
import isec
import time
		
def ch2():
    intersection = 1
    e = 0
    for canvas in CANVAS:
        for light3 in light2:
            if isec.light_status(intersection,light[e]):
                canvas.itemconfig(light3, fill = color[light[e]])
            else:
                canvas.itemconfig(light3, fill = color2[light[e]])
            e = e+1
            if e == 6:
                e = 0
        intersection = intersection + 1
		
def statecycle(intersection, cs):
	
    state [cs] = STATE [state[cs]] [(isec.sense(intersection,'A1') or isec.sense(intersection,'C1')) ] [isec.sense(intersection,'B1')]
    if state [cs] == 0: # These if statments check state and
                   # assigns light statuses based on current state.
        isec.light_off(intersection,light[1]) #These lines are what change the lights
        isec.light_off(intersection,light[2]) #from onn and off. The variable is used to select
        isec.light_on(intersection,light[0])  #the different intersections. Each if statment 
        isec.light_off(intersection,light[4]) #makes different lights turn on.
        isec.light_off(intersection,light[5]) #The light [] is used to pass thru the dictionary
        isec.light_on(intersection,light[3])  #created above.
        time.sleep(1)
                
    elif state [cs] == 1:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[3])
        isec.light_on(intersection,light[5])
        time.sleep(2)
          
    elif state [cs] == 2:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[5])
        isec.light_off(intersection,light[3])
        isec.light_on(intersection,light[4])
        time.sleep(4)
       
    elif state [cs] == 3:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
        time.sleep(1)

    elif state [cs] == 4:
        
        isec.light_off(intersection,light[0])
        isec.light_off(intersection,light[1])
        isec.light_on(intersection,light[2])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
        time.sleep(2)      
        
    elif state [cs] == 5:
        
        isec.light_off(intersection,light[2])
        isec.light_off(intersection,light[0])
        isec.light_on(intersection,light[1])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
        time.sleep(4)
    ch2()
    isec.print_lights()
 	
def autocycle ():

    e = 0
    for a in range(1,6):	    
        statecycle(a,e)
        e = e + 1
		
STATE = [[[1 , 1],[ 1, 1]], #This is the array
         [[ 1 , 1],[ 2, 2]], #That controls the state, of the Finite state machine
         [[ 3, 3], [ 3, 3]], #States are reassgned based on the current state, and 
         [[ 4, 4], [ 4, 4]], #two sensor values.
         [[ 4, 5], [ 4, 5]], #This is a 3d array.
         [[ 0, 0], [ 0, 0]]] #

#light = {1:'AR', 2:'AY', 3:'AG', 4:'BR', 5:'BY', 6:'BG'} #This the dictionary used to reference lights on an intersection, (I'm lazy)
light = ['AR','AY','AG','BR','BY','BG']
color = {'AR':'#FF0000','AY':'yellow','AG':'green','BR':'#FF0000','BY':'yellow','BG':'green'}
color2 = {'AR':'#920000','AY':'#A29C04','AG':'darkgreen','BR':'#920000','BY':'#A29C04','BG':'darkgreen'}
state = [0,0,0,0,0]

isec.simulate_hardware = True #Turns on simulation software.
isec.sensor_value_from_user = False #Allows user to enter sensor data.
isec.hw_init() # Initializes the software.

root = Tk()

root.title ('Light Control System')
root.geometry ('1200x600')

frame1 = Frame(root)
frame1.grid(row=0,column=0)
Light1 = Canvas(frame1, width=200, height=300, bg='white')  
Light1.grid(row = 2, column = 0)                
        

CANVAS = [Light1]

for a in CANVAS:
    AR= a.create_oval(5, 5, 95, 95, width=5, fill='red')
    AY= a.create_oval(5, 105, 95, 195, width=5, fill='white')
    AG= a.create_oval(5, 205, 95, 295, width=5, fill='white')
    BR= a.create_oval(105, 5, 195, 95, width=5, fill='white')
    BY= a.create_oval(105, 105, 195, 195, width=5, fill='yellow')
    BG= a.create_oval(105, 205, 195, 295, width=5, fill='white')
	
light2 = [AR,AY,AG,BR,BY,BG]

Label(frame1, text='1', font=('helvetica', 20, 'underline italic')).grid(row=0,column=0)

Label(frame1, text='A                       B', font = 50).grid(row=1,column=0)

Button(frame1, text = 'Change Intersection 1', command = lambda: statecycle(1,0)).grid(row = 4, column=0)

root.mainloop()
