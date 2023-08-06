import os

from colored import fg
from boxing import boxing
import inquirer

from pou.core.sleepy_colors import YELLOW_COLOR, WHITE_COLOR, RESET
from pou.core.storage import Storage, BOX_COLOR, HIGHLIGHT_COLOR, TEXT_COLOR

class Terminal():

    def __init__(self):
        box_color = Storage.load(BOX_COLOR)
        highlight_color = Storage.load(HIGHLIGHT_COLOR)
        text_color = Storage.load(TEXT_COLOR)

        if box_color == None: box_color = YELLOW_COLOR
        if highlight_color == None: highlight_color = YELLOW_COLOR
        if text_color == None: text_color = WHITE_COLOR

        self.BOX_COLOR = box_color
        self.HIGHLIGHT_COLOR = highlight_color
        self.TEXT_COLOR = text_color

    def box_text(self, text : str):
        self.clear()
        self.print(boxing(text))

    def selection(self, title : str, question : str, selections):
        try:
            self.clear()
            self.print(boxing(title))

            questions = [inquirer.List('input', message=self.colorize_text(question), choices=selections, carousel=True)]
            user_input = inquirer.prompt(questions)["input"]
        except:
            raise KeyboardInterrupt
        
        return user_input
    
    def input(self, title : str, question : str):
        self.clear()

        self.print(
            boxing(title)
        )

        print(f"{question}\n> ", end="")
        return input()

    def colorize_text(self, text : str):
        return f"{fg(self.TEXT_COLOR)}{text}{fg(self.TEXT_COLOR)}"

    def print(self, text : str, end : str = "\n", sep : str = ""):
        to_replace = "┌─┐│└─┘"
        for char in to_replace:
            text = text.replace(char, f"{fg(self.BOX_COLOR)}{char}{fg(self.TEXT_COLOR)}")
        print(self.colorize_text(text), end=end, sep=sep)
        print(RESET, end="", sep="")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')