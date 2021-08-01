from web_driver import WebDriver, skribblr_state_enum
import sys

if __name__ == "__main__":
    print("sdfsd")
    if (len(sys.argv) == 1):
        print("Please provide room ID")
        exit()


    # test_openCV()
    # exit()

    driver = WebDriver()
    
    # driver.get_image("test")
    # exit()

    driver.join_room(sys.argv[1], False)
    while not driver.state == skribblr_state_enum.PLAYING:
        driver.check_game_is_running()
    
    while driver.state == skribblr_state_enum.PLAYING:
        to_draw = driver.check_player_turn()
        if to_draw:
            driver.get_image(to_draw)
            print("ending now")
            exit()
        

