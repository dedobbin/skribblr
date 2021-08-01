from web_driver import WebDriver, skribblr_state_enum
import sys

if __name__ == "__main__":
    print("sdfsd")
    if (len(sys.argv) == 1):
        print("Please provide room ID")
        exit()

    driver = WebDriver()
    
    # driver.get_image("test")
    # exit()

    driver.participate(sys.argv[1])

