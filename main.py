import time

import cv2
import numpy as np
import pyautogui
import pyperclip


class GravityBot:
    words = {}

    meteor_image_path = r"images/meteor.png"
    meteor_image = cv2.imread(meteor_image_path)

    console_image_path = r"images/console.png"
    console_image = cv2.imread(console_image_path)

    start_image_path = r"images/start.png"
    start_image = cv2.imread(start_image_path)

    input_image_path = r"images/input.png"
    input_image = cv2.imread(input_image_path)

    timeout = 150

    console_code = r"setTimeout(() => {let words = '';let elements = document.getElementsByClassName('GravityTerm-text');for (const element of elements) {let child = element.firstChild;words += child.innerHTML + ';;';}navigator.clipboard.writeText(words);}, $timeout$);"

    empty_pos = ()
    start_pos = ()
    console_pos = ()
    input_pos = ()

    last_words = ""

    def __init__(self, words: dict):
        for k, v in words.items():
            self.words.update({k: v, v: k})

        self.console_code = self.console_code.replace("$timeout$", str(self.timeout))
        pass

    def screenshot(self):
        img = pyautogui.screenshot()
        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image

    def meteor_on_screen(self):
        pos = pyautogui.locateOnScreen(self.meteor_image_path, region=(
            0, int(pyautogui.size()[1] / 3), pyautogui.size()[0], int(pyautogui.size()[1] / 2)))
        return pos is not None, pos

    def get_start_pos(self):
        pos = pyautogui.locateOnScreen(self.start_image_path)
        if pos is not None:
            self.empty_pos = (pos.left, pos.top)
            self.start_pos = self.empty_pos
        else:
            print("Waring: Start pos not found")

    def get_console_pos(self):
        pos = pyautogui.locateOnScreen(self.console_image_path)
        if pos is not None:
            self.console_pos = (pos.left + pos.width, pos.top + (pos.height / 2))
        else:
            print("Waring: Console pos not found")

    def get_input_pos(self):
        pos = pyautogui.locateOnScreen(self.input_image_path)
        if pos is not None:
            self.input_pos = (pos.left + pos.width, pos.top + (pos.height / 2))
        else:
            print("Waring: Input pos not found")

    def get_words(self):
        pyautogui.click(self.console_pos[0], self.console_pos[1])

        pyperclip.copy(self.console_code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        pyautogui.click(self.empty_pos[0], self.empty_pos[1])

        while pyperclip.paste() == self.console_code:
            pass

        return str(pyperclip.paste()).split(";;")

    def run(self):
        first_iteration = True

        # setup
        # self.get_start_pos()
        self.get_console_pos()

        # start
        print("Ready. You can start now.")
        # pyautogui.click(self.start_pos[0], self.start_pos[1])

        # mainloop
        while True:
            self.get_console_pos()
            m_on_screen, pos = self.meteor_on_screen()
            if m_on_screen:
                if first_iteration:
                    first_iteration = False
                    self.empty_pos = pyautogui.position()
                self.last_words = self.get_words()
            else:
                self.last_words = []

            if self.last_words != "":
                self.run_input()

    def run_input(self):
        for word in self.last_words:
            if word != '':
                other = self.words[word]
                pyperclip.copy(other)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')

        self.last_words = []


class GravityBot2:
    words = {}

    console_image_path = r"images/console.png"

    timeout = 2000
    console_code = ""
    console_pos = ()
    empty_pos = ()

    new_words = []
    clipboard = ""

    def __init__(self, words: dict, code_file: str):
        for k, v in words.items():
            self.words.update({k: v, v: k})

        file = open(code_file, 'r')
        self.console_code = file.read()
        self.console_code = self.console_code.replace("$timeout$", str(self.timeout))
        file.close()

    def get_console_pos(self):
        pos = pyautogui.locateOnScreen(self.console_image_path)
        if pos is not None:
            self.console_pos = (pos.left + pos.width, pos.top + (pos.height / 2))
        else:
            print("Waring: Console pos not found")

    def run(self):
        print("Put ur mouse on a empty spot")
        print("u got 5 seconds")
        time.sleep(5)
        self.empty_pos = pyautogui.position()
        print("go")

        # init
        self.get_console_pos()
        pyautogui.click(self.console_pos[0], self.console_pos[1])
        pyperclip.copy(self.console_code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        pyautogui.click(self.empty_pos[0], self.empty_pos[1])

        while pyperclip.paste() == self.console_code:
            pass

        # run
        running = True
        while running:
            if str(pyperclip.paste()) != self.clipboard:
                self.clipboard = str(pyperclip.paste())
                n_words = self.clipboard.split(";;")
                self.new_words.extend(n_words)

            self.solve_one()

    def solve_one(self):
        if len(self.new_words) > 0:
            word = self.new_words[0]
            if word != '':
                print(self.new_words)
                print(word)
                other = self.words[word]

                pyautogui.write(other)
                pyautogui.press('enter')

            self.new_words = list(filter(word.__ne__, self.new_words))


if __name__ == '__main__':
    words = {
        "Auseinandersetzung, Streit": "argument",
        "Kreuzfahrt, Schiffsreise": "cruise",
        "stören": "disturb",
        "Taucher/Taucherin": "diver",
        "sich (zer)streiten": "fall out",
        "Erwärmung der Erdatmosphäre": "global warming",
        "jedoch": "however",
        "glücklicherweise": "luckily",
        "Verschmutzung": "pollution",
        "leider": "sadly",
        "leiden (unter)": "suffer (from)",
        "deshalb, darum": "that's why",
        "bedrohen, drohen": "threaten",
        "unglaublich": "unbelievable",
        "Menge": "amount",
        "meiden, vermeiden": "avoid",
        "konsumieren, zu sich nehmen": "consume",
        "zurzeit, momentan": "currently",
        "schaden, Schaden zufügen": "harm",
        "ignorieren, nicht beachten": "ignore",
        "Überfischen": "overfishing",
        "Politiker/Politikerin": "politician",
        "Meeresfrüchte": "seafood",

    }

    bot = GravityBot2(words, "code_2.js")
    bot.run()
