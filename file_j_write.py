import numpy as np
import time
from delta_kynametics import *
import json

import math
from socket import *
import time
import sys
import json

# Import the Decimal class from the decimal module
from decimal import Decimal

x_origin = 246-389
y_origin = -232+305
z_origin = -491
pre_x = -220

address = ('169.254.245.1', 5000)  # match arduino IP + port
client_socket = socket(AF_INET, SOCK_DGRAM)
print(address)
client_socket.settimeout(5)  # wait up to 5 seconds



# Create a 2D array with 3 rows and 4 columns

count = 0

#while ():  #get the image

filepath = '/Users/amithnalherath/Desktop/Curtin/Internship/Vsion/Angle detection/Block Mapping updated/robot_test (1).txt'
print("Python")
print(filepath)

def offset(x,y):
    if(float(x) < 0):
        R = math.sqrt(abs((float(x))*abs(float(x)))+abs((float(y))*abs(float(y))))
        Com_Z = R*28/350
        return Com_Z

    if(float(y) < 0):
        R = math.sqrt(abs((float(x))*abs(float(x)))+abs((float(y))*abs(float(y))))
        Com_Z = R*28/350
        return Com_Z

    else:
        R = math.sqrt(abs((float(x))*abs(float(x)))+abs((float(y))*abs(float(y))))
        Com_Z = R*28/200
        return Com_Z

offset_XY = 0.8*0.9091
t=0.3


# x_cord =0
# y_cord =0
# z_cord =0   
#

i = True
j=False

while True:

    while i==True:
        #Capture photo
        count=0
        print("Get Coordinates")
        
        x = -220  #camera X Input
        y = 220  #camera Y Input
        z = -491
        offset(x,y)
        coordinate = inverse(float(x)/offset_XY,float(y)/offset_XY,float(z)+offset(x,y))

        a = round(coordinate [1],2)
        b = round(coordinate [2],2)
        c = round(coordinate [3],2) 
        print("")
        print('X' + str(x) + ' Y' + str(y) + ' Z' + str(z))
        print('a =', a,'b =',b,'c =',c,'F =',60,'A =',40)
        client_socket.sendto(('a' + str(a) + ' b' + str(b) + ' c' + str(c) + ' F' + str(60) + ' A' + str(40)).encode(), address)
                
        time.sleep(0.6)

        exec(open("working.py").read())

        with open("cords.json", "r") as g:
            cords = json.load(g)

        data2 = cords[count]   
        x_cord2 =float(data2[0])
        pre_x = x_cord2 

        if pre_x == -220:
            print("nothing------")
            break


     
        i=False
        j=True

    while j==True:

        data = cords[count]   
        x_cord =float(data[0])
        y_cord =float(data[1])
        z_cord =data[2]

        print(cords)
        num_values = len(cords)   
        print('###############')

        x_cord = (x_cord-389)*1
        y_cord = (y_cord-305)*-1

        print(x_cord,y_cord)

        if 220>=x_cord >=-220:
                x_cord = x_cord 
                y_cord = y_cord                 
        else:
            x_cord = 220
            y_cord = -220
            print('out of bounds')
             
        if 220>=y_cord >=-220:
            x_cord = x_cord             
            y_cord = y_cord 
        else: 
            x_cord = 220            
            y_cord = -220
            print('out of bounds')






        print(len(cords)) 
        data = cords[count]
        #print(" X:" , data[0] , " Y:" , data[1] , " Z:" , data[2])
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                # client_socket.sendto(("{}".format(line.strip())).encode(), address)
                txt = "{}".format(line.strip())
                a = txt.split()
                if 4 < len(a): #check the array location is availbe 
                    F = a[3].split("F", 1)
                    A = a[4].split("A", 1)
                if a:
                    if (a[0])[0] == 'X' :
                        x = a[0].split("X", 1)
                        y = a[1].split("Y", 1)
                        z = a[2].split("Z", 1)

                        if x[1] == 'x':
                            # edit the value for the camera input value
                            x[1] = y_cord  #camera X Input
                            y[1] = x_cord  #camera Y Input
                            z[1] = z_cord
                            offset(x[1],y[1])
                            coordinate = inverse(float(x[1])/offset_XY,float(y[1])/offset_XY,float(z[1])+offset(x[1],y[1]))

                            a = round(coordinate [1],2)
                            b = round(coordinate [2],2)
                            c = round(coordinate [3],2) 
                            print("")
                            print('X' + str(x[1]) + ' Y' + str(y[1]) + ' Z' + str(z[1]))
                            print('a =', a,'b =',b,'c =',c,'F =',F[1],'A =',A[1])
                            client_socket.sendto(('a' + str(a) + ' b' + str(b) + ' c' + str(c) + ' F' + str(F[1]) + ' A' + str(A[1])).encode(), address)
                            time.sleep(t)


                        elif x[1] == 'd':
                            # edit the value for the camera input value
                            x[1] = y_cord  #camera X Input
                            y[1] = x_cord  #camera Y Input
                            z[1] = z_cord-30
                            offset(x[1],y[1])
                            coordinate = inverse(float(x[1])/offset_XY,float(y[1])/offset_XY,float(z[1])+offset(x[1],y[1]))

                            a = round(coordinate [1],2)
                            b = round(coordinate [2],2)
                            c = round(coordinate [3],2) 
                            print("")
                            print('X' + str(x[1]) + ' Y' + str(y[1]) + ' Z' + str(z[1]))
                            print('a =', a,'b =',b,'c =',c,'F =',F[1],'A =',A[1])
                            client_socket.sendto(('a' + str(a) + ' b' + str(b) + ' c' + str(c) + ' F' + str(F[1]) + ' A' + str(A[1])).encode(), address)
                            time.sleep(t)
                            
                        else:
                            offset(x[1],y[1])
                            coordinate = inverse(float(x[1])/offset_XY,float(y[1])/offset_XY,float(z[1])+offset(x[1],y[1]))
                            a = round(coordinate [1],2)
                            b = round(coordinate [2],2)
                            c = round(coordinate [3],2) 
                            
                            print("")
                            print('X' + str(x[1]) + ' Y' + str(y[1]) + ' Z' + str(z[1]))
                            print('a =', a,'b =',b,'c =',c,'F =',F[1],'A =',A[1])
                            client_socket.sendto(('a' + str(a) + ' b' + str(b) + ' c' + str(c) + ' F' + str(F[1]) + ' A' + str(A[1])).encode(), address)
                            time.sleep(t)
                    else:
                        if (a[0])[0] == "A" :
                            a = txt.split()
                            gr = a[1]
                            delay = a[3]
                            if gr == "TRUE":
                                print("AT")
                            if gr == "FALUSE":
                                print("AF")
                            time.sleep(int(delay)/1000)
        # Increment the counter by 1
        count += 1
        with open('cords.json', 'w') as f:
            # Write an empty list or dictionary to the file
            json.dump([[x_origin,y_origin,z_origin]], f)
        #file
        # If the count is equal to 10, break the loop
        if count == num_values:
                i = True
                j=False



    #     # some JSON data
    # data = {
    #     "a": a,
    #     "b": b,
    #     "c": c,
    #     "F": F[1],
    #     "A": A[1],
    #     # "Angle":angle
    # }

    # # open a file for writing
    # with open("data.json", "w") as outfile:
    #     # write the data to the file
    #     json.dump(data, outfile)              
