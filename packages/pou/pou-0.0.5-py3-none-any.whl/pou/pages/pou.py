from colored import fg

from pou.core.terminal import Terminal

from pou.pages.settings import Settings
from pou.pages.chatgpt import ChatGPT

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


class Pou():
    def __init__(self):
        self.terminal = Terminal()
        self.quit = False

    def chatgpt(self):
        ChatGPT(self.terminal).start()
        pass

    def settings(self):
        Settings(self.terminal).start()
        pass

    def exit(self):
        self.quit = True
        self.terminal.box_text(f"See you {fg(self.terminal.HIGHLIGHT_COLOR)}soon!{fg(self.terminal.TEXT_COLOR)}")
        pass

    def configure_user_cred(self):
        ChatGPT(self.terminal).configure_user_cred()

    def run(self):
        user_input = self.terminal.selection(
            f"Welcome to {fg(self.terminal.HIGHLIGHT_COLOR)}pou",
            f"What would {fg(self.terminal.HIGHLIGHT_COLOR)}you{fg(self.terminal.TEXT_COLOR)} like to do today? ",
            [f"{fg(self.terminal.TEXT_COLOR)}Back to Terminal",
             f"{fg(self.terminal.TEXT_COLOR)}Configure user credentials",
             f"{fg(self.terminal.TEXT_COLOR)}Settings", 
             f"{fg(self.terminal.TEXT_COLOR)}Exit"]
        )

        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Start": self.chatgpt()
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Configure user credentials": self.configure_user_cred()
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Settings": self.settings()
        if user_input == f"{fg(self.terminal.TEXT_COLOR)}Exit": self.exit()

    def start(self):
        self.chatgpt()
        while not self.quit:
            try:    
                self.run()
            except KeyboardInterrupt: self.exit()