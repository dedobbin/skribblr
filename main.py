import sys
import cv2
from web_driver import WebDriver
from img import img_show, img_resize, vectorize


if __name__ == "__main__":
    print("sdfsd")
    if (len(sys.argv) == 1):
        print("Please provide room ID")
        exit()

    # driver = WebDriver()
    # driver.participate(sys.argv[1])

    img = cv2.imread('/home/dozer/Pictures/recreated.png')
    vectorize(img)


    # img = driver.get_image("test")
    # #img = cv2.imread('/home/dozer/Pictures/green.png')
    # img = img_resize(img, 300, 300)
    # #driver.do_draw(img)
    # img_show(img)



