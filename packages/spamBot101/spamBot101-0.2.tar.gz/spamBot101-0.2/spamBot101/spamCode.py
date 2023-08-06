import pyautogui
import time
import logging
import keyboard

class spamBot:
    def __init__(self, message, interval):
        self.message = message
        self.interval = interval
        logging.info("SpamBot initialized!! Put the cursor on the chat box and wait for 5 seconds.")

    def spam(self):
        time.sleep(5)
        message = self.message
        n = 0
        interval = self.interval
        while n!=interval:
            pyautogui.typewrite(self.message)
            pyautogui.press("enter")
            n = n+1
            # if a key is pressed, stop the spam
            if keyboard.is_pressed("ctrl"):
                logging.info("SpamBot stopped!!")
                break
    
    def spamForever(self):
        logging.info("SpamBot started!!")
        while True:
            self.spam()
            # if a key is pressed, stop the spam
            if pyautogui.keyDown("ctrl"):
                logging.info("SpamBot stopped!!")
                break
    
    def spamForeverWithDelay(self, delay):
        logging.info("SpamBot started!!")
        while True:
            self.spam()
            time.sleep(delay)
            # if a key is pressed, stop the spam
            if pyautogui.keyDown("ctrl"):
                logging.info("SpamBot stopped!!")
                break

            