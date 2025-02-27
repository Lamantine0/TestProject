from tkinter import N
from typing import Self
from fastapi.templating import Jinja2Templates
import test




class Page_jinja:

    def __init__(self, templates = None):
        
        self.templates = templates
    
    def page(self):

        test = Jinja2Templates(directory="templates")

        self.templates = test

        return self.templates

page_jinja = Page_jinja()

page = page_jinja.page()

