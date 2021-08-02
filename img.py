import cv2

def img_resize(img, output_w, output_h):
    print("Resize image width to ", output_w, output_h)

    height, width = img.shape[:2]
    max_height = output_w
    max_width = output_h

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

def img_show(img):
    #img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    #img = cv2.imdecode(arr, -1)
    cv2.imshow('====== S K R I B B L R ====== ', img)
    if cv2.waitKey() & 0xff == 27: quit()