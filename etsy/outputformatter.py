from jinja2 import Template


class OutputFormatter:
    """
    Handles the outputting of the data to a file.
    
    Handles formatting in either html or json
    """
    
    def __init__(self, words_list, mode, file_path):
        """
        
        """
        self.words_list = words_list
        self.mode = mode
        self.file_path = file_path

    def output_html(self):
        error_free = [i for i in self.words_list if i.error == None]            
        errors = [i for i in self.words_list if i.error != None]
        with open("./template.jinja") as templateFile:
            template = Template(templateFile.read())

        print(template.render(error_free_shops=error_free,
                                  error_shops = errors))        
        