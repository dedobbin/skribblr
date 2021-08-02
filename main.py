import sys
from web_driver import WebDriver, skribblr_state_enum
from img import img_show, img_resize


if __name__ == "__main__":
    print("sdfsd")
    if (len(sys.argv) == 1):
        print("Please provide room ID")
        exit()

    driver = WebDriver()

    #driver.participate(sys.argv[1])

    img = driver.get_image("test")
    img = img_resize(img, 200)
    img_show(img)
    driver.do_draw(img)


    # driver.join_room(sys.argv[1])
    # driver.take_turn("test")



