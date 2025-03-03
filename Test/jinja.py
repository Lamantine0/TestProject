from fastapi.templating import Jinja2Templates





class Page_jinja:

    def __init__(self, templates = None):
        
        self.templates = templates
    
    def page(self):

        test = Jinja2Templates(directory="templates")

        self.templates = test

        return self.templates

page_jinja = Page_jinja()

page = page_jinja.page()

