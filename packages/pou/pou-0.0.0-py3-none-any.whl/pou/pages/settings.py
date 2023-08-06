from colored import fg
import re

from pou.core.terminal import Terminal
from pou.core.sleepy_colors import RED_COLOR, ORANGE_COLOR, YELLOW_COLOR, GREEN_COLOR, AQUAMARINE_COLOR, LAVENDER_COLOR, PURPLE_COLOR, WHITE_COLOR
from pou.core.storage import Storage, BOX_COLOR, TEXT_COLOR, HIGHLIGHT_COLOR

class Settings():

    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.quit = False

    def is_color_hex_code(self, text : str):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', text)
        return match

    def color_custom(self):
        user_input = self.terminal.input("Custom color", "Input the color's hexcode (e.g #fff)")
        while not self.is_color_hex_code(user_input):
            user_input = self.terminal.input("Custom color", "Make sure to enter a valid color hexcode (e.g #fff)")
        
        return user_input

    def color(self, title : str):
        user_input = self.terminal.selection(
            title, 
            "What color would you like to change it to?", 
            [f"{fg(WHITE_COLOR)}Blank white{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(RED_COLOR)}Milk blood red{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(ORANGE_COLOR)}Citrus Juice Orange{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(YELLOW_COLOR)}Sunshine Yellow{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(GREEN_COLOR)}Fresh Vegetable Green{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(AQUAMARINE_COLOR)}Idunnowhat Blue{fg(self.terminal.TEXT_COLOR)}",   
             f"{fg(LAVENDER_COLOR)}Fragrant Lavender{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(PURPLE_COLOR)}Grape purple{fg(self.terminal.TEXT_COLOR)}",
             f"{fg(self.terminal.TEXT_COLOR)}Custom"             
            ]
        )

        if user_input == f"{fg(WHITE_COLOR)}Blank white{fg(self.terminal.TEXT_COLOR)}": return WHITE_COLOR
        if user_input == f"{fg(RED_COLOR)}Milk blood red{fg(self.terminal.TEXT_COLOR)}": return RED_COLOR
        if user_input == f"{fg(ORANGE_COLOR)}Citrus Juice Orange{fg(self.terminal.TEXT_COLOR)}": return ORANGE_COLOR
        if user_input == f"{fg(YELLOW_COLOR)}Sunshine Yellow{fg(self.terminal.TEXT_COLOR)}": return YELLOW_COLOR
        if user_input == f"{fg(GREEN_COLOR)}Fresh Vegetable Green{fg(self.terminal.TEXT_COLOR)}": return GREEN_COLOR
        if user_input == f"{fg(AQUAMARINE_COLOR)}Idunnowhat Blue{fg(self.terminal.TEXT_COLOR)}": return AQUAMARINE_COLOR
        if user_input == f"{fg(LAVENDER_COLOR)}Fragrant Lavender{fg(self.terminal.TEXT_COLOR)}": return LAVENDER_COLOR
        if user_input == f"{fg(PURPLE_COLOR)}Grape purple{fg(self.terminal.TEXT_COLOR)}": return PURPLE_COLOR
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Custom": return self.color_custom()
        return "#fff"
    
    def back(self):
        self.quit = True

    def run(self):
        user_input = self.terminal.selection(
            "Settings", 
            f"What would you like to {fg(self.terminal.HIGHLIGHT_COLOR)}change?{fg(self.terminal.TEXT_COLOR)}", 
            [f"{fg(self.terminal.TEXT_COLOR)}Text color", 
             f"{fg(self.terminal.TEXT_COLOR)}Box color", 
             f"{fg(self.terminal.TEXT_COLOR)}Highlight color", 
             f"{fg(self.terminal.TEXT_COLOR)}Back"]
        )

        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Text color": 
            self.terminal.TEXT_COLOR = self.color("Text color")
            Storage.store(TEXT_COLOR, self.terminal.TEXT_COLOR)
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Box color": 
            self.terminal.BOX_COLOR = self.color("Box color")
            Storage.store(BOX_COLOR, self.terminal.BOX_COLOR)
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Highlight color": 
            self.terminal.HIGHLIGHT_COLOR = self.color("Highlight color")
            Storage.store(HIGHLIGHT_COLOR, self.terminal.HIGHLIGHT_COLOR)
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Back": 
            self.back()

    def start(self):
        while not self.quit:
            self.run()
