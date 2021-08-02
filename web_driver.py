from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver import ActionChains
import numpy as np
import requests
import time
from enum import Enum
from random import randrange
from PIL import Image
import base64
import io
from img import img_resize, img_show, img_create

class skribblr_state_enum(Enum):
    NONE = 0
    WAITING_TO_START = 1
    PLAYING = 1
    DRAWING = 2

class WebDriver:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.state = skribblr_state_enum.NONE
        time.sleep(1)
    
    #Will join room and take it's turn in a loop #TODO: catch keyboard exception so can snap out when calling manually
    def participate(self, room_id):
        self.join_room(room_id, False)
        while not self.state == skribblr_state_enum.PLAYING:
            self.check_game_is_running()
        
        while self.state == skribblr_state_enum.PLAYING:
            to_draw = self.check_player_turn()
            if to_draw:
                self.take_turn(to_draw)
            
    def take_turn(self, to_draw):
        print("Taking turn, should draw " + to_draw)
        img = self.get_image(to_draw)
        #img_show(img)
        x,y,w,h = self.get_canvas_dimensions()
        img = img_resize(img, w, h)
        img_show(img)
        self.do_draw(img, x, y)

    def do_draw(self, img, x = 0, y = 0):
        print("TODO: draw image to ", x, y)
        exit()

    def join_room(self, room_id, random_avatar = True):
        print("Joining room " + room_id)
        self.driver.get("https://skribbl.io/?" + room_id)
        try:
            accept_button = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'cmpboxbtnyes')))
            print("Cookie popup happend")
            accept_button.click()
        except TimeoutException:
            print("Cookie popup did NOT happen")

        time.sleep(0.2) #Wait for cookie pop up to go away

        #Set name
        input_field = self.driver.find_element_by_id("inputName")
        action = ActionChains(self.driver)
        action.move_to_element(input_field)
        action.click()
        action.send_keys('SKRIBBLR')
        action.perform()

        if random_avatar:
            #It gives you a randomizer button, why didn't i use that.. oh well    
            for i in range(3):
                button = self.driver.find_element_by_css_selector('.avatarArrowRight[data-avatarindex="'+ str(i) +'"]')
                for j in range(randrange(10)):
                    button.click()
                    time.sleep(0.1)

        self.driver.find_element_by_css_selector(".loginPanelContent .btn-success").click()
        self.state = skribblr_state_enum.WAITING_TO_START

    def check_game_is_running(self, wait_time = 3600):
        print("Waiting for game to start")
        try:
            input_chat = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#screenGame:not([style="display:none;"])')))
            self.state = skribblr_state_enum.PLAYING
            return True
        except TimeoutException:
            return False

    def check_player_turn(self, wait_time = 3600):
        if (self.state != skribblr_state_enum.PLAYING):
            print("Checking for turn when not playing makes no sense")
            return
        print ("Waiting for turn")
        #check if overlay is active with:
        #document.querySelector('#overlay:not([style="opacity: 0; display: none;"])')
        
        try:
            word_container = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#overlay:not([style*="display: none"]):not([style*="display: none"] .wordContainer:not([style="display: none;"])')))
            
            time.sleep(1)
            answers = self.driver.find_elements_by_css_selector('.wordContainer > .word')
            if (len(answers) == 0):
                # Because the WebDriverWait query is very janky, it can trigger on some transitions, 
                # very annoying to test because of the short time these screens are active, just do it this ugly way
                # although in respect i probably could have halted script execution to test... 
                print("FALSE POSITIVE, thought it was it's turn but it's not")
                return False
            #print("debug", answers[0])
            print("Should select a word")
            i = randrange(2)
            time.sleep(1)
            answer = answers[i].get_attribute('innerText')
            #TODO: should get image from other tab here, takes quite some time, can wait with selecting perhaps
            answers[i].click()
            print("Selected " + answer)
            self.state = skribblr_state_enum.DRAWING
            return answer
        except TimeoutException:
            return False

    def get_image(self, search_query):
        self.driver.execute_script('''window.open("https://www.google.com/","_blank");''')
        #self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
        #self.driver.execute_script('''window.open("https://images-go''' + "TEEEEST" + '''ogle.com/","_blank");''')
        #self.driver.get("https://www.google.com")
        
        prev_handle = self.driver.current_window_handle
        
        #Find what is index of current tab, select one after that to get to newly opened tab..
        window_index = -1
        for i in range(len(self.driver.window_handles)):
            if self.driver.window_handles[i] == prev_handle:
                window_index = i
                break
        self.driver.switch_to.window(self.driver.window_handles[window_index+1])

        # Cookie popup, kinda nasty to detect so just spam 'accept' no matter if its there or not until we are pretty sure we can use the page
        should_have_clicked = False
        while not should_have_clicked:
            buttons = self.driver.find_elements_by_css_selector('button')
            #print(len(buttons))
            if (len(buttons) > 1):
                print("Cookie popup maybe happend")
                for b in buttons:
                    #print(b.get_attribute('innerText'))
                    #We are not sure if pop up is actually active, or will active, just spam it to get rid of it
                    #TODO: should work for english too
                    if "akkoord" in b.get_attribute('innerText'):
                        for i in range(3):
                            try:
                                b.click()
                            except ElementNotInteractableException:
                                #Tells us element could not be scrolled into view when clicked,but works just fine?? oh well, let's march on
                                pass
                            time.sleep(0.1)
                        should_have_clicked = True
                        
            time.sleep(0.1)

        print("Should have passed cookie wall now")

        #input query
        input_field = self.driver.find_element_by_css_selector("input")
        action = ActionChains(self.driver)
        action.move_to_element(input_field)
        action.click()
        action.send_keys(search_query)
        action.send_keys(Keys.ENTER) 
        action.perform()
        time.sleep(1)

        #Find 'images' button
        all_a = self.driver.find_elements_by_css_selector("a")

        image_link = None
        for a in all_a:
            #TODO: should also work in english..
            if "Afbeeldingen" in a.get_attribute("innerText"):
                image_link = a.get_attribute("href")
                break

        #switch to image search
        if not image_link:
            print("Could not find image link, aborting........")
            return None
        
        self.driver.get(image_link)

        #<img src="data:image/jpeg;base64
        #[jsaction^="click"] img[src^="data"]'
        #Pick first image from grid
        try:
            img = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[jsaction^="click"] img[src^="data"]')))
        except TimeoutException:
            print("Could not find image, aborting........")
            return None
        
        img.click()

        #Get url of actual image from slide in
        time.sleep(1) #It seems when you go too fast, you end up with base64 encoded image data, not sure why this happens and if this actualy fixes it..
        try:
            img = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[rel="noopener"] img')))
        except TimeoutException:
            print("Could not find image, aborting........")
            return None

        #print("TODO: load image: " + img.get_attribute("src"))
        #TODO: finish

        #print(img.get_attribute("src"))
        url = img.get_attribute("src")
        if ("data:image" in url):
            print("TODO: handle base64 encoded images", url)
            # resp = requests.get(img.get_attribute("src").strip()).content
            # base64_decoded = base64.b64decode(resp)
            # image = Image.open(io.BytesIO(base64_decoded))
            # image = np.array(image)
            # return image
            return None
    
        #resp = requests.get(url, stream=True).raw
        resp = requests.get(url, stream=True).raw
        img_data = np.asarray(bytearray(resp.read()), dtype="uint8")
        #image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        img = img_create(img_data)
        #Restore original tab TODO: close
        self.driver.switch_to.window(prev_handle)

        return img

    def get_canvas_dimensions(self):
        print("Getting canvas dimensions")
        e = self.driver.find_element_by_id("canvasGame")
        #todo: return offset
        return [ e.location['x'], e.location['x'], e.size['width'],e.size['height'] ]

    def test(self):
        self.driver.get("http://www.python.org")
        assert "Python" in self.driver.title
        elem = self.driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source
        #self.driver.close()
        return True