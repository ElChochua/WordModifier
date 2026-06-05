import json
import sys
from os import path

def get_resource_path(relative_path):
    
    if hasattr(sys, '_MEIPASS'):

        base_path = sys._MEIPASS
    else:

        base_path = path.abspath(path.dirname(__file__))
    
    return path.join(base_path, relative_path)

language_file_path = get_resource_path(path.join("config", "lang.json"))

class LanguageManager:
    def __init__(self, default_language="es", language_file=language_file_path):
        self.language_file = language_file
        
        with open(self.language_file, "r", encoding="utf-8") as f:
            self.text = json.load(f)
            
        self.set_language(default_language)
        
    def set_language(self, language_code):
        if language_code in self.text:
            self.current_language = language_code
            
    def get(self, key):
        return self.text[self.current_language].get(key, key)