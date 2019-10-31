import numpy as np
import cv2
import math
import pytesseract

def bubbleSort(arr):
    n = len(arr)
 

    for i in range(n):
        for j in range(0, n-i-1):

            if arr[j][0] > arr[j+1][0] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
def overlap(x, y, w, h, x1, y1, w1, h1):

    if (   (x1+w1) < (x+w)
        and (x1) > (x)
        and (y1) > (y)
        and (y1+h1) < (y+h)
        ):
        return True;
    
    else:
        return False;
    

def dfs(mat, pos):
    global cnt
    for j in range(0,length):
        if mat[pos][j] == 1:
            cnt = cnt + 1
            dfs(mat, j)

            
def checkChildExists(rectangles, child, mat):
    lp = 0
    pos = -1
    for i in rectangles:
        if i == child:
            pos = lp
            break
        lp = lp + 1     
    if pos != -1:
        total = 0
        for i in range(0, len(rectangles)):
             total = total + mat[pos][i]
    return pos,total           
inc = 0
def cropImage(img, j):
    global inc
    crop_img = img[j[1]:j[1]+j[3], j[0]:j[0]+j[2]]
    print(j)
    cv2.imwrite("images/cropped"+str(inc)+".png", crop_img) 
    inc = inc + 1            
    value = (pytesseract.image_to_string(crop_img, lang='eng'))
    return value
    
    
    
def buildBFSCode(mat, root, rectangles, image, L, imVisited):
    global init
    pics =["first0.jpeg","first1.jpeg","first2.jpeg","first3.jpeg","first4.jpeg","first5.jpeg"]
    
    
    dict ={"parent":"<div class='parent' name='parent' style='height:hp;width:100%;'>P</div>" , 
           "parentB":"<div class='parentB' name='parent' style='height:hp;width:100%;box-shadow:none'>P</div>"  
           ,
           "row":"<div class='parent'  name='row' style='width:100%;height: hr;box-shadow:none'>R</div> " 
           
           ,"child":"<div class='parent'  name='child' style='height:hc;width: wc'>CHILD</div> ", 
           
           "image":"<div style='height:hcv;width:100%;background:url(first0.jpeg) no-repeat;background-size: cover;'></div>",
          
            "p":"<p>para</p>",
           
           "head":"<h1>head</h1>"
          }
    
    #constructing parent
    if init:
        parent = dict["parent"];
        init= False
    else:
        parent = dict["parentB"];
    pHeight = tempRects[root][3]
    parent = parent.replace("hp",str(round(pHeight)))
  
        
        
    rowStringList = ""
    
    temp = []
    loop = 0

    
    
    

    for j in rectangles:
        if mat[root][loop] == 1:
            temp.append(j) 
            L.put(loop)
        loop = loop + 1 
   
    y = []
    for i in temp:
        y.append(i[1])
    
    if len(y) > 0:
        y.sort()   
        visited= [False]  * len(temp)
        for i in y:
            print(i)            
            row =[]
            innerLoop = 0
            totalWidth = 0
            totalHeight = 0
            
            for j in temp:
                if ( i == j[1]  or (i <= j[1] + 20   and  i >= j[1] - 20 )) and not visited[innerLoop]:

                    row.append(j)
                    visited[innerLoop] = True
                    totalWidth += j[2]
                    totalHeight += j[3]
               


                innerLoop = innerLoop + 1
            bubbleSort(row)
            
            
            if len(row) > 0:
                rowString = dict["row"]
                
                #constructing row
                
                
                # for each row construct row
                avgHeight = totalHeight / len(row)
                rowString = rowString.replace("hr",str(round(avgHeight)))
                
                
                
                childStringList = ""
                for j in row:
                    
                    
                    childString = dict["child"]
                    parentLoc, childCnt = checkChildExists(rectangles, j, mat)
                    
                    childString = childString.replace("hc",str(round(avgHeight))+"px")
                    childString = childString.replace("wc",str(round((j[2] * 100) / totalWidth)-5 )+"%")
                    
                    if childCnt == 0:
                        findChildValueString = cropImage(img, j)
                        if len(findChildValueString) == 0:
                                childValueString = dict["image"]
                                childValueString = childValueString.replace("hcv",str(round(avgHeight))+"px")
                                
                                for k in range(0,len(imVisited)):
                                    if not imVisited[k]:
                                        imVisited[k] = True
                                        childValueString = childValueString.replace("first0.jpeg",pics[k])
                                        break
                        else:
                                if "-"  in findChildValueString:
                                    childValueString = dict["p"]
                                    childValueString=childValueString.replace("para",findChildValueString)
                                elif "+"  in findChildValueString:
                                    childValueString = dict["head"]
                                    childValueString=childValueString.replace("head",findChildValueString)
                                    
                        
                        
                        
                        childString = childString.replace("CHILD",childValueString)
                        
                    else:
                        childString = childString.replace("CHILD","replace"+str(parentLoc))
                    

                    childStringList = childStringList + childString;
                    cv2.rectangle(image, j, (255,0,0), 2)
                    
                rowString = rowString.replace("R",childStringList)     
                rowStringList = rowStringList + rowString
    else:
        
        return "none"
    parent = (parent.replace("P",rowStringList))  
    return parent
        


        

       
            

img = cv2.imread('images/test8.png')
image = cv2.imread('images/test8.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
ret,thresh = cv2.threshold(gray,127,255,1)
 
contours,h = cv2.findContours(thresh,1,2)
rectangles = [] 
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
   
    if len(approx)==5:
        cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        tmp =cv2.boundingRect(cnt)
        if tmp[2] >50 and tmp[3] >50:
            rectangles.append( cv2.boundingRect(cnt))
        cv2.rectangle(img, cv2.boundingRect(cnt), (255,0,0), 2)
        
    elif len(approx) == 9:
        cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        cv2.drawContours(img,[cnt],0,(0,255,255),-1)

rectangles  = (set(rectangles)) 
# all distict rectangles in given input
print(rectangles)
length = len(rectangles)
mat = [[0 for x in range(length)] for y in range(length)] 

oLoop = 0
for i in rectangles:
    init = False
    minArea = 0
    rs =(0,0,0,0)
    iLoop = 0
    index = -1
    for j in rectangles:
            if oLoop != iLoop:
                if overlap(j[0],j[1],j[2],j[3],i[0],i[1],i[2],i[3]):
                    a2 = j[2] * j[3]
                    a1 = i[2] * i[3]
                    if a1 < a2 :
                        if not init:
                            minArea = a2 - a1
                            rs = j
                            init = True
                            index =iLoop
                        elif a2 - a1 < minArea:
                            minArea = a2 -a1
                            rs = j
                            index =iLoop
                           
            iLoop = iLoop + 1      
    if index != -1:        
          mat[index][oLoop] = 1 


      
    oLoop= oLoop + 1    
 
print(mat)
root = -1
for i in range(0,length):
    cnt =1
    dfs(mat,i)
    if cnt == length:
        root = i
        break       
tempRects =[]
for i in rectangles:
    tempRects.append(i)
    
cv2.rectangle(image, tempRects[root], (255,0,0), 2)        
import queue   
L = queue.Queue()  
finalString ="<html>  <link rel='stylesheet' href='styles.css'> <link href='https://fonts.googleapis.com/css?family=Verdana' rel='stylesheet'><div class='header'><span class='headerText'>draw.webapp.io</span></div><body id= 'body' style='display: flex;justify-content: center;width:100%;flex-direction: row;flex-wrap: wrap;'>"+"replace"+str(root)+"</body></html>"

    




inc = 0
imVisited = [False,False,False,False,False,False]
init = True

if root != -1:
        L.put(root)

        while not L.empty():
            rmov = L.get()
            rs = buildBFSCode(mat,rmov, rectangles, image, L,imVisited)
            if rs != "none":
                finalString=  finalString.replace("replace"+str(rmov),rs)
   
print(finalString)
file1 = open("file.html","w") 
file1.write(finalString)
file1.close()
cv2.imwrite('images/y.png', img) 
cv2.imwrite('images/final.png', image) 

