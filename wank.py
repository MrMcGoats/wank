#!/usr/bin/env python3

from time import sleep
from sys import argv
import random

usage="""Usage: wank.py [options]

        --speed=<num/fast|slow>               Speed at which to jerk it, in seconds, or 'fast' or 'slow' 
        --len=<num>                           Length of the shaft. Must be at least 4
        --handed=<ambidextrous|lefty|righty>  Hand to masturbate with. Default is right.
        --sto=<num>                           Up-strokes to orgasm
        -k                                    Don't erase the final frame of the animation (default)
        -nk                                   Erase the final frame of the animation
        --velocity=<num>                      The number of spaces between the cock and the ejaculate
        -h, --help                            Display usage and exit."""

length=4       #length of shaft
cum_speed=5    #number of strokes to acheive orgasm
jerk_speed=0.2 #number of seconds to wait between redrawing the penis with new hand placement
cum_distance=1 #Number of spaces between cock and cum shot

two_handed=False
lefty=False

keep_last_cock=True

for i in argv:
    if i=="--help" or i=="-h":
        print(usage)
        exit(0)
        
    elif i[:8]=="--speed=":
        if i[8:]=="fast":
            jerk_speed=0.2
        elif i[8:]=="slow":
            jerk_speed=0.4
        else:
            try:
                jerk_speed=float(i[8:])
            except ValueError:
                print(usage)
                exit(1)
                
    elif i[:6]=="--len=":
        try:
            length=int(i[6:])
            if length<4:
                print("Size doesn't matter and all that, but Jesus Christ!")
                exit(1)
        except ValueError:
            print(usage)
            exit(1)
        
    elif i[:9]=="--handed=":
        if i[9:]=="ambidextrous":
            two_handed=True
        elif i[9:]=="lefty":
            lefty=True
        elif i[9:]=="righty":
            lefty=False
        else:
            print(usage)
            exit(1)
    
    elif i=="lefty":
        if two_handed:
            lefty=True
        else:
            print(usage)
            exit(1)
            
    elif i[:6]=="--sto=":
        try:
            cum_speed=int(i[6:])
        except ValueError:
            print(usage)
            exit(1)
            
    elif i=="-k":
        continue
    elif i=="-nk":
        keep_last_cock=False
    
    elif i[:11]=="--velocity=":
        try:
            cum_distance=int(i[11:])
        except ValueError:
            print(usage)
            exit(1)
            
    elif i==argv[0]:
        continue
    else:
        print(usage)
        exit(1)
        
if length<6:
    two_handed=False
    
#Prevent dick burn
if jerk_speed<0.1:
    jerk_speed=0.1
    
#Dynamically generate animation frames based on given shaft length
base_frame="8"
for i in range(0,length):
    base_frame+="="
base_frame+="D"

def set_hand_pos(shaft_spot,frame):
    if ((shaft_spot>=len(frame) or shaft_spot<=1) and not two_handed) or ((shaft_spot>=len(frame) or shaft_spot<=3) and two_handed):
        return frame
    
    frame=list(frame)
    
    finger='m'
    finger_l='w'
    if lefty:
       finger='w' 
       finger_l='m'

    if two_handed:
        frame[shaft_spot+1]=finger_l
        frame[shaft_spot]=finger_l
        frame[shaft_spot-2]=finger
        frame[shaft_spot-3]=finger
    else:
        frame[shaft_spot]=finger
        frame[shaft_spot-1]=finger
    
    return "".join(frame)

def get_next_frame(frames,prev):
    if (prev%len(frames))==len(frames)-1:
        return frames[0]
    else:
        return frames[(prev%len(frames))+1]

jerk_frames=[]

start_val=2
if two_handed:
    start_val=4
    length-=1
    
for i in range(start_val,length):
    jerk_frames.append(set_hand_pos(i,base_frame))
for i in range(length,start_val,-1):
    jerk_frames.append(set_hand_pos(i,base_frame))
    
if two_handed:
    length+=1

#cum_frames = [jerk_frames[len(jerk_frames-1)]+(" "*cum_distance)]
cum_frames = ["-",
        jerk_frames[0]+"--"]

cum_seperator = " "

if cum_distance > 1:
    distance_since_last_stain = 0
    for i in range(1, cum_distance + 1):
        seperator = " "
        if distance_since_last_stain % random.randint(1,100) == 0:
            seperator = "."
        distance_since_last_stain += 1
        cum_frames.append(get_next_frame(jerk_frames, i) + cum_seperator + seperator + "---")
        cum_seperator += seperator

cum_frames.append(get_next_frame(jerk_frames, cum_distance + 1) + cum_seperator + "--_")
cum_frames.append(get_next_frame(jerk_frames, cum_distance + 1) + cum_seperator + "___")

for i in range(2,length*4):
    cum_frames.append(get_next_frame(jerk_frames,i))
    
if length>=20:
    cum_speed=2

try:
    for i in range(0,cum_speed):
        for j in jerk_frames:
            print(j,end="\r")
            sleep(jerk_speed)
except KeyboardInterrupt:
    print("\rOh, you fucking tease!")
    exit(0)
  
try:
    for i in cum_frames:
        print(i,end="\r")
        sleep(0.1)

    if keep_last_cock:
        print(cum_frames[len(cum_frames)-1])
except KeyboardInterrupt:
    print()
    exit(0)
