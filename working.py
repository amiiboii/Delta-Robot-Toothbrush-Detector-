import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
import numpy as np
import time
import sys, getopt
import re
import math
import sqlite3  
from prettytable import PrettyTable
import json

x_origin = -220
y_origin = 220
z_origin = -521
threshold_value = 130

o=0
coor = np.array([['0','9'],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9],[0,9]])
coordibate = np.array([0,9,0])




def intersect1d_padded(x):
    x, y = np.split(x, 2)
    padded_intersection = -1 * np.ones(x.shape, dtype=np.int)
    intersection = np.intersect1d(x, y)
    padded_intersection[:intersection.shape[0]] = intersection
    return padded_intersection

def rowwise_intersection(a, b):
    return np.apply_along_axis(intersect1d_padded,
                    1, np.concatenate((a, b), axis=1))
                    
def drawAxis(frame, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
 
  ## [visualization1]
  angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv.line(frame, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv.line(frame, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv.line(frame, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
  ## [visualization1]
  return p
 
def getOrientation(pts, frame):
  ## [pca]
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]

  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 

  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
  ## [pca]
 
  ## [visualization]
  # Draw the principal components
  cv.circle(frame, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  yolo = drawAxis(frame, cntr, p1, (255, 255, 0), 1)
  drawAxis(frame, cntr, p2, (0, 0, 255), 5)

 
  angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
  

#   if loc > 0:
#     angle2 = angle - np.deg2rad(180)
#   else:
#     angle2 = angle


  angle = np.rad2deg(-angle)

  print(angle)


  if angle >= (-134) and angle <= 0:
        print('hello')
        angle = angle + (180)


  # Label with the rotation angle
  #label = "  Rotation Angle: " + str(-int(np.rad2deg(angle2))) + " degrees" 
  #textbox = cv.rectangle(frame, (cntr[0], cntr[1]-25), (cntr[0] + 250, cntr[1] + 20), (255,255,255), -10)
  #cv.putText(frame, label, (cntr[0], cntr[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)   
  return [mean/1.7,angle]

def sorting(x_cord,y_cord,x_origin,y_origin):


    x_squred = (x_cord-(x_origin*-1))**2
    y_squred = (y_cord-(y_origin*-1))**2
    length = sqrt(x_squred+y_squred)
    return(length)

def countours():
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_head = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Convert image to binary
    _, bw = cv.threshold(gray, threshold_value, 255, cv.THRESH_BINARY )
    _, bw_head = cv.threshold(gray_head, threshold_value, 255, cv.THRESH_BINARY )
    
    # Find all the contours in the thresholded image
    contours, hierarchy = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    contours_head, hierarchy = cv.findContours(bw_head, cv.RETR_LIST, cv.CHAIN_APPROX_NONE) 

            # Was the image there?``
    if frame is None:
        print("Error: Camera not detected")
        exit(0)

    return(contours_head)

def headtresh():

    templates = []
    for i in range(1, 20):
        template = cv.imread('template_{}.png'.format(i))
        templates.append(template)

    # Set the initial match flag to False
    match_found = False

    # Loop through each template and perform template matching
    for template in templates:
        result = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED)

        # Find the minimum and maximum values and their locations
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # If the match is good enough, set the match flag to True and draw a rectangle around the matched area
        threshold = 0.79
        if max_val > threshold:
            match_found = True
            h, w = template.shape[:2]
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(frame, top_left, bottom_right, (0,255,0), 2)

    # If no match was found, display a message
    if not match_found:
        cv.putText(frame, 'No match found', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv.LINE_AA)


    return(max_val)    

def admenting():
    cordinates=np.round(returns[0], decimals=0)
    angle = np.round(returns[1], decimals=2)   

    x_cordinate = str(cordinates).split()
    x_cordinate_strip = str(x_cordinate[0]).strip("[] ")
    # print(x_cordinate_strip) 
    y_cordinate_strip = str(x_cordinate[1]).strip("[] ")

    x_cordinate_strip = x_cordinate_strip.strip('')
    y_cordinate_strip = y_cordinate_strip.strip('')



    if x_cordinate_strip =='':
        x_cordinate_strip=10


    x_cordinate_1 = float(x_cordinate_strip)    
    y_cordinate_1 = float(y_cordinate_strip) 


    return angle, x_cordinate_strip, y_cordinate_strip, x_cordinate_1, y_cordinate_1    

       

def rect_detection():
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Use Canny edge detection to detect edges in the frame
    edges = cv.Canny(gray, 50, 150)

    # Find contours in the edge frame
    _, contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cv.imwrite('Output_Image1.jpg',edges)        

    # Iterate through the contours and approximate each one as a polygon
    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

        # If the approximated polygon has four vertices, it is a rectangle
        if len(approx) == 4:
            # Check if the rectangle is a long rectangle
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = w / h
            if aspect_ratio > 1.5:
                # Draw the long rectangle on the frame
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

x_set = set()
y_set = set()

# connect to the database
conn = sqlite3.connect('points.db')

# create a cursor
cursor = conn.cursor()

# drop the existing Points table
cursor.execute('DROP TABLE Points;')

# create the new Points table
cursor.execute('''
    CREATE TABLE Points (
        ID INTEGER PRIMARY KEY,
        X REAL,
        Y REAL,
        Angle REAL,
        Distance REAL
    );
''')

# create a table object
table = PrettyTable()

# add columns to the table
table.field_names = ["ID", "X", "Y", "Angle", "Distance"]

video_capture = cv.VideoCapture(0)

ret, frame = video_capture.read()

cv.imwrite('image.jpg',frame)
frame = cv.imread('image.jpg')

contours_head = countours()

for a, b in enumerate(contours_head):

    # Calculate the area of each contour
    area_head = cv.contourArea(b)
    
    # Ignore contours that are too small or too large
    if area_head < 3000 or 20000 < area_head:
        arears = area_head
        continue
    
    # Draw each contour only for visualisation purposes
    cv.drawContours(frame, contours_head, a, (0, 255, 255), 10)

    
    

    # Find the orientation of each shape
    returns = getOrientation(b, frame)

    angle, x_cordinate_strip, y_cordinate_strip, x_cordinate_1, y_cordinate_1   = admenting()

    length = sorting(x_cordinate_1,y_cordinate_1,x_origin,y_origin)



    print(angle)

    length = np.round(length, decimals=0)  


    # headtresh()
    # rect_detection()

    # insert the new point into the table
    cursor.execute('''
        INSERT INTO Points (X, Y, Angle, Distance)
        VALUES (?, ?, ?, ?);
    ''', (x_cordinate_strip, y_cordinate_strip, angle, length))

    # commit the changes to the database
    conn.commit()

    # # query the table and add the rows to the table
    cursor.execute('SELECT * FROM Points;')
    for row in cursor.fetchall():
        table.add_row(row)

    # table.sortby = "Distance"   


    #print(table)

    # Create a cursor
    cursor = conn.cursor()

    # Execute the SELECT statement
    cursor.execute('SELECT * FROM Points')

    rows = cursor.fetchall()

    arrays = []




    # clear the table
    table.clear_rows()

    # define the DELETE query
    query = '''
    DELETE FROM Points
    WHERE Distance IN (
    SELECT Distance
    FROM Points
    GROUP BY Distance
    HAVING COUNT(*) > 1
    );
    '''

    # execute the DELETE query
    cursor.execute(query)                


    conn.commit()


    # Loop through the rows
    for row in rows:
        # Convert the tuple to a list and append it to the arrays list
        arrays.append(list(row))

    cord_arr = map(lambda x: [x[2], x[3]], arrays)
    cord_arr = list(cord_arr)


    # if done ==1:
            
            
    z_cord = -550 

    cord_l = map(lambda x: x.append(z_cord), cord_arr)
    cord_l1 = list(cord_l)

    row_count = len(cord_arr)


    if b.all() <= 0:
        result = map(lambda x: [x_origin, y_origin, z_origin], cord_arr)

        # Convert the map object to a list
        cord_arr = list(result)
        with open("cords.json", "w") as f:
            json.dump(cord_arr, f)        
        

    # result = map(lambda x: [x_cordinate_strip, y_cordinate_strip, z_origin], cord_arr)
    # cord_arr = list(result)

    # # print(x_cordinate_strip,y_cordinate_strip)

    cord = cord_arr

    xy = np.array([[x_cordinate_strip,y_cordinate_strip]])
    # print(xy)

    arr_list = xy.tolist()

    coor[o] = np.array(arr_list)

    o=o+1

    arr2 = coor[0:o]
    arr3 = arr2.tolist()

    for sublist in arr3:
    # Append the new element to the end of each sublist
        sublist.append(z_cord)

    
    print(arr3)
    
    with open("cords.json", "w") as f:
        json.dump(arr3, f)

 
    



    cv.imshow('Output Image', frame)

# print(area_head)    

# if area_head <= 0:
#     print('hello')
#     none_array = np.array([[x_origin,y_origin,z_origin]])
#     none_array = none_array.tolist()


#     with open("cords.json", "w") as f:
#         json.dump(none_array, f)    




key = cv.waitKey(1)


