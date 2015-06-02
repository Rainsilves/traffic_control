from Tkinter import*
import isec
import time
		
def ch2():
    for (intersection,canvas) in enumerate(CANVAS):
        for (e,light3) in enumerate(light2):
            if isec.light_status((intersection + 1),light[e]):
                canvas.itemconfig(light3, fill = color[light[e]])
            else:
                canvas.itemconfig(light3, fill = color2[light[e]])
		
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
        
                
    elif state [cs] == 1:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[3])
        isec.light_on(intersection,light[5])
        
          
    elif state [cs] == 2:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[5])
        isec.light_off(intersection,light[3])
        isec.light_on(intersection,light[4])
        
       
    elif state [cs] == 3:
        
        isec.light_off(intersection,light[1])
        isec.light_off(intersection,light[2])
        isec.light_on(intersection,light[0])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
        

    elif state [cs] == 4:
        
        isec.light_off(intersection,light[0])
        isec.light_off(intersection,light[1])
        isec.light_on(intersection,light[2])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
                
        
    elif state [cs] == 5:
        
        isec.light_off(intersection,light[2])
        isec.light_off(intersection,light[0])
        isec.light_on(intersection,light[1])
        isec.light_off(intersection,light[4])
        isec.light_off(intersection,light[5])
        isec.light_on(intersection,light[3])
    ch2()
    isec.print_lights()
 	
def autocycle ():
    e = 0
    for a in range(1,6):	    
        statecycle(a,e)
        e = e + 1
		
STATE = [[[1 , 1],[ 1, 1]], #This is the array
         [[ 1 , 2],[ 1, 2]], #That controls the state, of the Finite state machine
         [[ 3, 3], [ 3, 3]], #States are reassgned based on the current state, and 
         [[ 4, 4], [ 4, 4]], #two sensor values.
         [[ 4, 4], [ 5, 5]], #This is a 3d array.
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
frame2 = Frame(root)
frame2.grid(row=0, column=1)
frame3 = Frame(root)
frame3.grid(row=0, column=2)
frame4 = Frame(root)
frame4.grid(row=0, column=3)
frame5 = Frame(root)
frame5.grid(row=0, column=4)
    
Light1 = Canvas(frame1, width=200, height=300, bg='white')  
Light1.grid(row = 2, column = 0)                

Light2 = Canvas(frame2, width=200, height=300, bg='white')  
Light2.grid(row = 2, column = 2)                

Light3 = Canvas(frame3 , width=200, height=300, bg='white')  
Light3.grid(row = 2, column = 4)                

Light4 = Canvas(frame4, width=200, height=300, bg='white')  
Light4.grid(row = 2, column = 6)                

Light5 = Canvas(frame5, width=200, height=300, bg='white')  
Light5.grid(row = 2, column = 8)                

CANVAS = [Light1, Light2, Light3, Light4, Light5]

for a in CANVAS:
    AR= a.create_oval(5, 5, 95, 95, width=5, fill='red')
    AY= a.create_oval(5, 105, 95, 195, width=5, fill='white')
    AG= a.create_oval(5, 205, 95, 295, width=5, fill='white')
    BR= a.create_oval(105, 5, 195, 95, width=5, fill='white')
    BY= a.create_oval(105, 105, 195, 195, width=5, fill='yellow')
    BG= a.create_oval(105, 205, 195, 295, width=5, fill='white')
	
light2 = [AR,AY,AG,BR,BY,BG]

Label(frame1, text='1', font=('helvetica', 20, 'underline italic')).grid(row=0,column=0)
Label(frame2, text='2', font=('helvetica', 20, 'underline italic')).grid(row=0,column=2)
Label(frame3, text='3', font=('helvetica', 20, 'underline italic')).grid(row=0,column=4)
Label(frame4, text='4', font=('helvetica', 20, 'underline italic')).grid(row=0,column=6)
Label(frame5, text='5', font=('helvetica', 20, 'underline italic')).grid(row=0,column=8)
Label(frame1, text='A                       B', font = 50).grid(row=1,column=0)
Label(frame2, text='A                       B', font = 50).grid(row=1,column=2)
Label(frame3, text='A                       B', font = 50).grid(row=1,column=4)
Label(frame4, text='A                       B', font = 50).grid(row=1,column=6)
Label(frame5, text='A                       B', font = 50).grid(row=1,column=8)

Button(frame1, text = 'Change Intersection 1', command = lambda: statecycle(1,0)).grid(row = 4, column=0)
Button(frame2, text = 'Change Intersection 2', command = lambda: statecycle(2,1)).grid(row = 4, column=2)
Button(frame3, text = 'Change Intersection 3', command = lambda: statecycle(3,2)).grid(row = 4, column=4)
Button(frame4, text = 'Change Intersection 4', command = lambda: statecycle(4,3)).grid(row = 4, column=6)
Button(frame5, text = 'Change Intersection 5', command = lambda: statecycle(5,4)).grid(row = 4, column=8)
Button(root, text = 'Auto', command = autocycle).grid(row = 1, column=0)
Button(root, text = 'Change color', command = ch2).grid(row = 1, column=1)

root.mainloop()
