from web_driver import WebDriver, skribblr_state_enum
import sys

if __name__ == "__main__":
    print("sdfsd")
    if (len(sys.argv) == 1):
        print("Please provide room ID")
        exit()

    driver = WebDriver()
    driver.take_turn("test")

    # img = driver.get_image("test")
    # print(img)

    # driver.participate(sys.argv[1])

