import os
import json
import logging
import requests
import traceback

from colored import fg

from pou.core.terminal import Terminal
from pou.core.storage import Storage

CHATGPT_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_MODEL = "gpt-3.5-turbo"

ORGANIZATION_KEY = "organization_key"
API_KEY = "api_key"

class ChatGPT():
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.quit = False
        self.user_credentials = {ORGANIZATION_KEY: Storage.load(ORGANIZATION_KEY), API_KEY: Storage.load(API_KEY)}
    
    def shell(self):
        self.terminal.clear()
        if self.user_credentials[ORGANIZATION_KEY] == None or self.user_credentials[API_KEY] == None: self.configure_user_cred()
        
        self.terminal.box_text("Terminal")
        self.terminal.print(f"Write commands! (Type {fg(self.terminal.HIGHLIGHT_COLOR)}exit{fg(self.terminal.TEXT_COLOR)} to leave)")
        self.terminal.print(f"Available {fg(self.terminal.HIGHLIGHT_COLOR)}sleepychat{fg(self.terminal.TEXT_COLOR)} commands")
        self.terminal.print(f"- {fg(self.terminal.HIGHLIGHT_COLOR)}ask{fg(self.terminal.TEXT_COLOR)} - To ask ChatGPT questions. Example: {fg(self.terminal.HIGHLIGHT_COLOR)}ask 'Hello world'{fg(self.terminal.TEXT_COLOR)}")
        self.terminal.print(f"- {fg(self.terminal.HIGHLIGHT_COLOR)}translate{fg(self.terminal.TEXT_COLOR)} - Translate text to a particular language. Example: {fg(self.terminal.HIGHLIGHT_COLOR)}translate english 'hello world'{fg(self.terminal.TEXT_COLOR)}")
        self.terminal.print(f"- {fg(self.terminal.HIGHLIGHT_COLOR)}menu{fg(self.terminal.TEXT_COLOR)} - To exit to menu. Example: {fg(self.terminal.HIGHLIGHT_COLOR)}menu{fg(self.terminal.TEXT_COLOR)}")
        self.terminal.print("")
        while True:
            # FIXME: This is ugly
            try:
                self.terminal.print("cwd: ", f"{fg(self.terminal.HIGHLIGHT_COLOR)}{os.getcwd()}\n")
                user_input = input(f"{fg(self.terminal.TEXT_COLOR)}> ")
                split_text = user_input.split(' ')
                split_text = list(filter(lambda text : len(text) > 0, split_text))

                if len(split_text) == 0: continue

                if split_text[0] == 'ask': self.ask(user_input[3:].strip())
                elif split_text[0] == 'menu': break
                elif split_text[0] == 'translate':
                    user_input.replace(split_text[0], '')
                    user_input.replace(split_text[1], '')
                    self.translate(user_input[10:].strip(), split_text[1])
                elif split_text[0] == 'cd': 
                    try: os.chdir(user_input[2:].strip())
                    except: self.terminal.print(f"The system cannot find the file specified: {user_input[2:].strip()}")
                else: os.system(user_input)
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as e: 
                logging.error(traceback.format_exc())

    def ask(self, question : str):
        payload = json.dumps({
            "model": CHATGPT_MODEL,
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7,
            "stream": True
        })
        res = None
        try:
            session = requests.Session()
            res = session.post(CHATGPT_URL, headers={
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {self.user_credentials[API_KEY]}",
                "OpenAI-Organization": self.user_credentials[ORGANIZATION_KEY]},
                data=payload, stream=True)
            
            gpt_response = ""
            for chunk in res.iter_content(chunk_size=512):
                data = chunk.decode('UTF-8')
                data = data.replace('data: ', '')
                data = data.strip()

                split_lines = data.split('\n')
                for line in split_lines:
                    line = line.strip()
                    if line == "": continue

                    if line == "[DONE]": break
                    
                    line = json.loads(line)
                    if "choices" in line.keys(): line = line["choices"]
                    if len(line) > 0: line = line[0]
                    if "delta" in line.keys(): line = line["delta"]
                    if "content" in line.keys(): line = line["content"]
                    else: line = ""
                    gpt_response += line
            
            curr_size = 0
            new_response = ""
            BOX_SIZE = os.get_terminal_size().columns - 35

            split_response = gpt_response.split(" ")
            for char in split_response:

                if curr_size != 0: new_response += " "
                if curr_size + len(char) > BOX_SIZE: 
                    curr_size = 0
                    new_response += "\n"
                
                new_response += char
                curr_size += len(char)

            self.terminal.box_text(f"{fg(self.terminal.HIGHLIGHT_COLOR)}ChatGPT's response:{fg(self.terminal.TEXT_COLOR)}\n{new_response}")
        except: 
            if res.status_code == 401: print("Wrong credentials")

    def translate(self, question : str, final_lang : str):
        self.ask(f"You are Google translate. Translate the following text to {final_lang}: {question}")

    def configure_user_cred(self):
        organization_key = self.terminal.input(f"{fg(self.terminal.TEXT_COLOR)}Organization key", f"{fg(self.terminal.TEXT_COLOR)}Enter your OpenAI {fg(self.terminal.HIGHLIGHT_COLOR)}organization key{fg(self.terminal.TEXT_COLOR)}. You can get that here: {fg(self.terminal.HIGHLIGHT_COLOR)}https://platform.openai.com/account/org-settings{fg(self.terminal.TEXT_COLOR)}")
        api_key = self.terminal.input("API key", f"{fg(self.terminal.TEXT_COLOR)}Enter your OpenAI {fg(self.terminal.HIGHLIGHT_COLOR)}API key{fg(self.terminal.TEXT_COLOR)}. You can get that here: {fg(self.terminal.HIGHLIGHT_COLOR)}https://platform.openai.com/account/api-keys{fg(self.terminal.TEXT_COLOR)}")
        
        self.user_credentials = {ORGANIZATION_KEY: organization_key, API_KEY: api_key}

        cache_login = self.terminal.selection(
            "Store credentials?",
            f"Would you like to {fg(self.terminal.HIGHLIGHT_COLOR)}store{fg(self.terminal.TEXT_COLOR)} your credentials for future use?",
            [f"{fg(self.terminal.TEXT_COLOR)}Yes",
             f"{fg(self.terminal.TEXT_COLOR)}No"])
        
        if cache_login == f"{fg(self.terminal.TEXT_COLOR)}Yes": 
            Storage.store(ORGANIZATION_KEY, organization_key)
            Storage.store(API_KEY, api_key)

        pass

    def start(self):
        self.shell()
