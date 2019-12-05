import numpy as np
import imageio
import random
# Cell States
# 0 = Clear, 1 = Fuel, 2 = Fire, 3 = Immune, 
#takes prob of fuel, total time, terrain parameters, random fire, immunity, and lightning
def mainprogram(prob, total_time, terrX, terrY, randomFire, percentImmunity, probLightning, nameOfGif):
    terrain_size = [terrX,terrY] # size of the simulation: terrX*terrY cells
    # states hold the state of each cell
    states = np.zeros((total_time,*terrain_size))
    # initialize states by creating random fuel and clear cells
    states[0] = np.random.choice([0,1],size=terrain_size,p=[1-prob,prob])
    #Sets the boundaries equal to 0
    #Code formatted for terrX rows and terrY columns
    for i  in range(terrX):
        states[0,i,0] = 0
        states[0,i,terrY-1] = 0
    for i in range(terrY):
        states[0,0,i] = 0
        states[0,terrX-1,i] = 0
        
        #If percentImmunity has a value
    if percentImmunity!=0:
        for i in range(terrain_size[0]):
            for g in range(terrain_size[1]):
                if states[0,i,g]==1:
                    xrand=random.uniform(0,1)
                    if xrand<=0.2:
                        states[0,i,g]=3
                        
    # set the middle cell on fire!!!
    if randomFire==0:
        states[0,terrain_size[0]//2,terrain_size[1]//2] = 2
    elif randomFire==1:
        #RANDOM GRID 
        x = round(random.uniform(1,terrain_size[0]-2))
        y = round(random.uniform(1,terrain_size[0]-2))
        states[0,x,y]=2
    else: #random chance of multiple trees catching fire, based on the random.uniform
        for i in range(1,terrain_size[0]-2):
            for g in range(1,terrain_size[0]-2):
                if states[0,i,g]==1:
                    if random.uniform(0,1)<randomFire:
                        states[0,i,g]=1
                    
    for t in range(1,total_time):
        # Make a copy of the original states
        states[t] = states[t-1].copy()
        if probLightning!=0:
            for f in range(terrain_size[0]):
                for g in range(terrain_size[1]):
                    if states[t,f,g]==1:
                        xrand=random.uniform(0,1)
                        if xrand<=probLightning:
                            states[t,f,g]=2
        
        for x in range(1,terrain_size[0]-1):
            for y in range(1,terrain_size[1]-1):
                if states[t-1,x,y] == 2: # It's on fire
                    states[t,x,y] = 0 # Put it out and clear it
                    # If there's fuel surrounding it
                    # set it on fire!
                    if states[t-1,x+1,y] == 1: 
                        states[t,x+1,y] = 2
                    if states[t-1,x-1,y] == 1:
                        states[t,x-1,y] = 2
                    if states[t-1,x,y+1] == 1:
                        states[t,x,y+1] = 2
                    if states[t-1,x,y-1] == 1:
                        states[t,x,y-1] = 2
                        colored = np.zeros((total_time,*terrain_size,3),dtype=np.uint8)

    # Color
    for t in range(states.shape[0]):
        for x in range(states[t].shape[0]):
            for y in range(states[t].shape[1]):
                value = states[t,x,y].copy()
    
                if value == 0:
                    colored[t,x,y] = [139,69,19] # Clear
                elif value == 1: 
                    colored[t,x,y] = [0,255,0]   # Fuel
                elif value == 2: 
                    colored[t,x,y] = [255,0,0]   # Burning
                elif value == 3:
                    colored[t,x,y] = [0,255,0]   # Immune but colored as fuel
        
    #This code outputs an array named fireArray, of length total_time that holds 
    #the amount of cells on fire for each timestep.
    #Not required, but cool!
    fireArray = np.zeros(total_time)    
    for w in range(total_time):         
        onfirerightnow = 0
        for i in range(terrain_size[0]):
            for g in range(terrain_size[1]):
                if states[w,i,g]==2:
                    onfirerightnow+=1
        fireArray[w]=onfirerightnow            
    nameOfGif += ".gif"          
    # Crop
    cropped = colored[:200,1:terrain_size[0]-1,1:terrain_size[1]-1]
    imageio.mimsave(nameOfGif, cropped)
#end of function
    #takes prob of fuel, total time, terrain parameters, random fire, immunity, and lightning
           #fuel,time,[x,  y],fire,immu,lightn, name
mainprogram(0.6, 300, 100, 100, 0, 0.2, 0.001, 'gif1')
#mainprogram(0.6, 300, 100, 100, 0, 0.2, 0.001, '2ndgifname')

#mainprogram(0.6, 300, 100, 100, 0.0015, 0, 0, 'gifnull1')
#mainprogram(0.6, 300, 100, 100, 0, 0.2, 0, 'gifA2')
#mainprogram(0.6, 300, 100, 100, 0, 0.5, 0, 'gifA5')
#mainprogram(0.6, 300, 100, 100, 0, 0.8, 0, 'gifA8')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.2, 0, 'gifB2')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.5, 0, 'gifB5')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.8, 0, 'gifB8')
#mainprogram(0.6, 300, 100, 100, 0, 0, 0.0015, 'gifnull0015)
#mainprogram(0.6, 300, 100, 100, 0, 0, 0.0001, 'gifnull0001')
#mainprogram(0.6, 300, 100, 100, 0, 0, 0.05, 'gifnull05')
#mainprogram(0.6, 300, 100, 100, 0, 0.2, 0.0015, 'gifDimmune2light0015')
#mainprogram(0.6, 300, 100, 100, 0, 0.5, 0.001, 'gifDimmune5light001')
#mainprogram(0.6, 300, 100, 100, 0, 0.8, 0.05, 'gifDimmune8light05')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0, 0.0015, 'gifClight0015')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0, 0.0001, 'gifClight0001')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0, 0.05, 'gifClight05')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.2, 0.0015, 'gifCimmune2light0015')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.5, 0.001, 'gifCimmune5light001')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.8, 0.05, 'gifCimmune8light05')
#mainprogram(0.6, 300, 100, 100, 0.02, 0.5, 1, 'gifcustom1')
#mainprogram(0.6, 300, 100, 100, 0.0015, 0.00001, 0.85, 'gifcustom2')
#mainprogram(0.6, 300, 100, 100, 1, 0.45, 0.000005, 'gifcustom3')

print("All scenarios have been run, and a video of each has been added to the project folder. If any videos had the same names they were overwritten.")
#code takes prob of fuel, total_time, terrain parameters, random fire start, immunity, and lightning
#prob fuel is the percent a given cell will start as fuel (1), otherwise the cell is clear (0)
#total_time is the amount of timesteps that will take place in the function
#terrX is the amount of rows for cells
#terrY is the amount of columns for cells
#randomFire is 0 if fire is wanted in center, 1 if fire is randomly placed in the grid, a number between 0 and 1 if you want random cells to start on fire.
#percentImmunity is a value between 0 and 1 that dictates if a cell is immune to fire if already fuel. 0 if no trees immune
#probLightning is a value between 0 and 1 that dictates if a cell will catch fire if fuel each timestep. This is to simulate a dry thunderstorm
#nameOfGif is a string that your scenario will save as in the projects folder. 
#If another gif with the same name exists, it will be overwritten with this gif. Do NOT put .gif at the end, code formats this automatically.
