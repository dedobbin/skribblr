import cv2

def img_resize(img, output_w):
    print("Resize image")
    #print(img.shape)

    scale_factor = output_w / img.shape[0]
    if scale_factor < 1:
        output_h = int(img.shape[1] * scale_factor)
    else:
        output_h = int(img.shape[1] / scale_factor)

    print("old: ", img.shape)
    print("new: ", str(output_w) + "," + str(output_h), scale_factor)

    dim = (output_w, output_h)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def img_create(data):
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return image

def img_show(img):
    #img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    #img = cv2.imdecode(arr, -1)
    cv2.imshow('====== S K R I B B L R ====== ', img)
    if cv2.waitKey() & 0xff == 27: quit()