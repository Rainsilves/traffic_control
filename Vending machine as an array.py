fsm = [[1, 2, 5],
       [2, 3, 6],
       [3, 4, 7],
       [4, 5, 8],
       [5, 6, 9],
       [6, 7, 10],
       [7, 8, 11],
       [8, 9, 12],
       [9, 10, 13],
       [10, 11, 14]]
state = 0

d = {'n':0, 'd':1, 'q':2, 'N':0, 'Q':2, 'D':1}
ch = {10:'nothing.', 11:'a nickel.',
      12:'a dime.', 13:'a dime and a nickel.',
      14:'two dimes.'}
uinput = input() ('enter n, d, q, or e:')
while uinput != 'e':
    if uinput not in d:
        print (' input not accepted, enter another input:')
    else:
        p = d [uinput]
        state = fsm [state] [p]
        print (state)
        if state >= 10:
            print ('here is your soda')
            print ('Your change is ', ch [state])
            state = 0
    uinput = input() ('enter n, d, q, or e:')
