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


if __name__ == '__main__':
    words = {
        "bouger": "(sich) bewegen",
        "courir": "laufen, rennen",
        "lancer": "werfen",
        "sauter": "springen, hüpfen",
        "nager": "schwimmen",
        "glisser": "gleiten",
        "pratiquer": "ausüben",
        "transpirer": "schwitzen",
        "la force": "die Kraft",
        "l'équilibre (m)": "das Gleichgewicht",
        "la sensation": "das Gefühl",
        "souple": "beweglich",
        "fort/forte": "stark",
        "Le but, c'est de...": "Das Ziel ist, zu...",
        "gagner": "gewinnen",
        "prendre du plaisir": "Spass haben",
        "se détendre": "sich entspannen",
        "devenir plus fort": "stärker werden",
        "rester en forme": "in Form bleiben / fit bleiben",
        "être équipé/-e de...": "ausgerüstet sein mit...",
        "la difficulté": "die Schwierigkeit",
        "difficile": "schwierig",
        "facile": "einfach, leicht",
        "seul/seule": "allein",
        "à deux, à trois...": "zu zweit, zu dritt...",
        "en groupe": "in Gruppen",
    }

    bot = GravityBot(words)
    bot.run()
