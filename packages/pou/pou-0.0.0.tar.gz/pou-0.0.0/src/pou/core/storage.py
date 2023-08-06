import os
import json

# STORAGE KEYS
BOX_COLOR = "box_color"
HIGHLIGHT_COLOR = "highlight_color"
TEXT_COLOR = "text_color"

class Storage():
    @staticmethod
    def store(key : str, value : str):
        folder_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'storage'))
        file_path = os.path.join(folder_path, 'config')

        if not os.path.exists(folder_path): os.mkdir(folder_path)
        
        data = {}
        if os.path.isfile(file_path): data = json.loads(open(file_path).read())
        data[key] = value

        open(file_path, 'w').write(json.dumps(data))

    @staticmethod
    def load(key : str):
        folder_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'storage'))
        file_path = os.path.join(folder_path, 'config')

        if not os.path.exists(folder_path): os.mkdir(folder_path)
        
        if os.path.isfile(file_path): 
            data = json.loads(open(file_path).read())
            if key in data.keys(): return data[key]
            else: return None
        else: return None