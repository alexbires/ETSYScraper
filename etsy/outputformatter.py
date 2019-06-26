import json
from jinja2 import Template


class HTMLOutput:
    """
    Handles the outputting of the data to a file.

    Handles formatting in either html or json
    """

    def __init__(self, words_list, file_path):
        """
            @param words_list: The list of ShopsAndWords objects
            @param file_path: The path to save the html to
        """
        self.words_list = words_list
        self.file_path = file_path

    def output_html(self):
        """
        Writes the template html to the file path located at self.file_path
        """
        error_free = [i for i in self.words_list if i.error is None]
        with open("./template.jinja") as template_file:
            template = Template(template_file.read())

        html_output = template.render(error_free_shops=error_free)
        if len(self.file_path) > 1:
            with open(self.file_path, "w") as html_file:
                html_file.write(html_output)
                print("File written successfully")


class JSONOutput:
    """
    Handles the outputting of important files as a json blob
    The json object will have a schema as follows:
        {
                "results":[
                        "shop_id": <shop_id>
                        "important_words": [
                                "word1",
                                "word2",
                                "word3",
                                "word4",
                                "word5"
                        ]
                ]
        }
    """

    def __init__(self, words_list):
        """
            @param words_list: The list of ShopsAndWords objects
        """
        self.words_list = words_list

    def output_json(self):
        """
        Outputs json to standard out
        """
        json_output = {"results":[]}
        for word_object in self.words_list:
            to_append = {"shop_id":word_object.shop_id,
                         "important_words":[]}

            for word in word_object.words_list:
                to_append["important_words"].append(word)
                json_output["results"].append(to_append)

        string_json = str(json_output)
        print(string_json.replace("'", "\"")) #hacky i'm aware
