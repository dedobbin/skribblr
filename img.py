import cv2
import numpy as np

def img_resize(img, output_w, output_h):
    height, width = img.shape[:2]
    max_height = output_w
    max_width = output_h

    resized = img
    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
        scaling_factor = max_height / float(height)
        if max_width/float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        resized = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return resized

def img_create(data):
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return image

def img_to_lines(img):
    src_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    src_gray = cv2.blur(src_gray, (3,3))
    
    threshold = 50
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # font = cv2.FONT_HERSHEY_COMPLEX
    lines = []
    for cnt in contours :
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        #cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 

        n = approx.ravel() 
        i = 0
        while i < len(n):
            if i + 3 >= len(n):
                # Point without end
                #print("contains single point", i, n)
                x = n[i]
                y = n[i + 1]
                lines.append([x, y])
            else:
                x1 = n[i]
                y1 = n[i + 1]
                x2 = n[i + 2]
                y2 = n[i + 3]
                lines.append([x1, y1, x2, y2])
            
            i+=4
              
    
    print(lines)
    return []            

    

def img_show(img):
    #img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    #img = cv2.imdecode(arr, -1)
    cv2.imshow('====== S K R I B B L R ====== ', img)
    if cv2.waitKey() & 0xff == 27: quit()