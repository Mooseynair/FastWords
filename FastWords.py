import cv2
import mss
import numpy as np
import pytesseract
import pyautogui
import time
import os


class FastWords:
    def __init__(self):
        self.SCT = mss.mss()
        self.dimensions = {
            'left': 800,
            'top': 130,
            'width': 300,
            'height': 50
        }

    def ReadScreen(self, debug=False):
        scr = self.SCT.grab(self.dimensions)
        img = np.array(scr)
        color = cv2.cvtColor(img, cv2.IMREAD_COLOR)

        # Only show if we are debugging
        if debug:
            cv2.imshow("The result", color)
            cv2.waitKey(0)

        path_tess = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = path_tess
        text = pytesseract.image_to_string(color)
        text = text.replace('\x0c', '').replace('[', '')
        if debug:
            if text == '':
                print("Nothing")
        return text

    def EndGame(self, click=False, debug=False):
        area = {
            'left': 600,
            'top': 830,
            'width': 650,
            'height': 170
        }
        scr = self.SCT.grab(area)
        img = np.array(scr)
        try_again = cv2.imread('TryAgain.png', cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(img, try_again, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if debug:
            print("Max val: ")
            print(max_val)
        if max_val > .85:
            if click:
                # print(max_loc[0] + area['left'], max_loc[1] + area['top'])
                left_adj = max_loc[0] + area['left']
                top_adj = max_loc[1] + area['top']
                pyautogui.click(left_adj, top_adj)
            return True
        return False

    def find_letter(self, letter):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(dir_path, f"Letters/{letter}.png")
        area = {
            'left': 630,
            'top': 250,
            'width': 700,
            'height': 700
        }

        max_val = 0
        try_count = 0
        while max_val < .95:
            scr = self.SCT.grab(area)
            img = np.array(scr)
            letter = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            result = cv2.matchTemplate(img, letter, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            try_count += 1
            # print(try_count)

            if try_count > 10000 or self.EndGame():
                print("Can't find it")
                time.sleep(3)
                y = list(max_loc)
                y[0] = 800
                y[1] = 400 
                max_loc = tuple(y)
                break

        left_adj = max_loc[0] + area['left'] + 5
        top_adj = max_loc[1] + area['top']+50
        pyautogui.click(left_adj, top_adj)


if __name__ == "__main__":
    # Testing class
    screen = FastWords()
    # screen.ReadScreen(True)
    screen.EndGame(click=True, debug=True)
    screen.find_letter("Z")
