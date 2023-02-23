# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:14:15 2023

@author: Shreyas
"""
row= int(input("Number of rows ? > "))
col= int(input("Number of columns ? > "))

arr = row*col
arrow = [chr(count) for count in range (ord('A'), ord('A')+row)]    
arcol = [str(count) for count in range (1,col+1)]
print(arrow)
print(arcol)
Wells = []
for i in range (0, row, 1):
    for j in range (0, col, 1):
        Wells.append(arrow[i]+arcol[j])



x = float(input("X dimensions ? > "))
y = float(input("Y dimensions ? > "))
distx = float(input("Distance between the wells, x > "))
disty = float(input("Distance between the wells, y > "))
z = float(input("height of the whole thing ?"))
xoff = float(input("X offset (center of first well from edge of the labware) ?>"))+11.5
yoff = float(input("Y offset (center of first well from edge of the labware)?>"))+16
depth = float(input("Depth of the well?>"))
print ("Generating locations for an array of  " + str (arr))
print ("of size " + str(x) + " and " + str(y))



with open ('array.txt','w') as file :

    for i in range (0,col,1):
        for j in range (0,row,1):
            
            file.write('\n\n"'+str(arrow[j]+arcol[i])+'" : {')
            file.write('\n\t''"depth": 0.1,')
            file.write('\n\t"totalLiquidVolume": 5,')
            file.write('\n\t"shape": "rectangular",') 
            file.write('\n\t"xDimension":'+str(x)+',')
            file.write('\n\t"yDimension":'+str(y)+',')
            file.write('\n\t"x":'+str(xoff + i*(x+distx))+',')
            file.write('\n\t"y":'+str(yoff + j*(y+disty))+',')
            file.write('\n\t"z":'+str(z)+'\n },')