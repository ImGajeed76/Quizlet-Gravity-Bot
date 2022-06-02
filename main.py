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

    console_code = r"setTimeout(() => {" \
                   r"let word = '';" \
                   r"let element = document.getElementsByClassName('GravityTerm-text');" \
                   r"let child = element[0].firstChild;" \
                   r"word = child.innerHTML;" \
                   r"navigator.clipboard.writeText(word);" \
                   r"}, $timeout$);"

    empty_pos = ()
    start_pos = ()
    console_pos = ()
    input_pos = ()

    last_word = ""

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
        pos = pyautogui.locateOnScreen(self.meteor_image_path)
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

    def get_word(self):
        pyautogui.click(self.console_pos[0], self.console_pos[1])

        pyperclip.copy(self.console_code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        pyautogui.click(self.empty_pos[0], self.empty_pos[1])

        word = str(pyperclip.paste())
        return word

    def run(self):
        # setup
        self.get_start_pos()

        # start
        pyautogui.click(self.start_pos[0], self.start_pos[1])

        # mainloop
        while True:
            self.get_console_pos()
            m_on_screen, pos = self.meteor_on_screen()
            if m_on_screen:
                self.last_word = self.get_word()
            else:
                self.last_word = ""

            if self.last_word != "":
                self.run_input()

    def run_input(self):
        other = self.words[self.last_word]
        pyperclip.copy(other)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')


if __name__ == '__main__':
    words = {
        "la tête": "der Kopf",
        "le cou": "der Hals",
        "le bras": "der Arm",
        "l'épaule (f)": "die Schulter",
        "le coude": "der Ellbogen",
        "la main": "die Hand",
        "le doigt": "der Finger",
        "le dos": "der Rücken",
        "la jambe": "das Bein",
        "le genou": "das Knie",
        "le pied": "der Fuss",
        "croiser": "kreuzen",
        "écarter": "spreizen, ausbreiten",
        "plier": "beugen, falten",
        "tendre": "strecken",
        "baisser": "senken",
        "lâcher": "loslassen",
        "arrêter": "aufhören",
        "recommencer": "wieder beginnen",
        "avancer": "nach vorne strecken",
        "reculer": "zurückziehen, zurückgehen",
        "danser": "tanzen",
        "se lever": "aufstehen",
        "Lève-toi.": "Steh auf.",
        "Levez-vous.": "Steht auf.",
        "s'asseoir": "sich setzen",
        "Assieds-toi.": "Setz dich.",
        "Asseyez-vous.": "Setzt euch.",
        "tenir": "halten",
        "Tiens...": "Halte...",
        "Tenez...": "Haltet...",
        "la plage": "der Strand",
        "la pluie": "der Regen",
        "le vent": "der Wind",
        "la neige": "der Schnee",
        "Tu t'en souviens?": "Erinnerst du dich daran?",
        "J'y pense souvent.": "Ich denke oft daran.",
        "J'en suis fier/fière.": "Ich bin stolz darauf.",
        "On en parle.": "Man spricht darüber.",
        "J'en ai besoin.": "Ich brauche es.",
        "Elle en profite.": "Sie profitiert davon.",
        "Je m'en fous.": "Das ist mir egal.",
        "Je n'en sais rien.": "Ich weiss nichts davon.",
        "Je n'y peux rien.": "Ich kann nichts dafür.",
        "On y va?": "Auf geht's!",
        "J'y vais.": "Ich mache mich auf den Weg.",
        "Vas-y!": "Los! / Mach schon!",
        "Allons-y!": "Auf geht's!",
        "On y est.": "Es ist so weit.",
        "Nous y sommes.": "Da wären wir.",
        "Ca y est.": "Es ist so weit.",
        "Va-t'en!": "Geh weg!",
        "On s'en va.": "Wir gehen jetzt.",
        "Le/La ... qui me plaît est...": "..., der mir gefällt, ist...",
        "Un/Une... qui me fascine est...": "..., der/die mich fasziniert, ist...",
        "Le/La... que je préfère est...": "..., den/die ich bevorzuge, ist...",
        "Le/La... que je trouve bien est...": "..., das ich gut finde, ist...",
    }

    bot = GravityBot(words)
    bot.run()
