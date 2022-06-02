import cv2
import numpy as np
import pyautogui
import pyperclip


class GravityBot:
    meteor_image_path = r"images/meteor.png"
    meteor_image = cv2.imread(meteor_image_path)

    console_image_path = r"images/"
    console_image = cv2.imread(console_image_path)

    console_code = r""

    def __init__(self):
        pass

    def screenshot(self):
        img = pyautogui.screenshot()
        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image

    def meteor_on_screen(self):
        pos = pyautogui.locateOnScreen(self.meteor_image_path)
        return pos is not None, pos

    def get_word(self):
        pyperclip.copy(self.console_code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        word = str(pyperclip.paste())


if __name__ == '__main__':
    bot = GravityBot()

    while True:
        bot.meteor_on_screen()
