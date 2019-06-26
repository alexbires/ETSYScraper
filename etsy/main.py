import re
import sys
import argparse
import request
import algorithm
import outputformatter


class Main:
    """
    Uses classes to scrape the Etsy API and process the results into
    an html report or a json object.
    """

    CODES = [
        "18680568", "15074008", "9004327",
        "11774051", "10019510", "19787744",
        "6207697", "14778674", "11248716",
        "8595827"]

    def __init__(self, api_key, std_in):
        """
        @param api_key: the api key for Etsy
        @param listings: a list of listings for data tracking purposes
        @param word_list: a list of word object to pass for output formatting
        """
        self.api_key = api_key
        self.std_in = std_in
        self.listings = []
        self.word_list = []

    def parse_arguments(self):
        """
        Parses the user given arguments and sets the appropriate user input
        """
        parser = argparse.ArgumentParser(
            description="Fetches a list of items from a particular Etsy\
                store and then displays them in a user specified output file.")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--api", action="store_true",
                           help="Enter in your API key")
        group.add_argument("--api-file",
                           help="Specify a file where your API key lives")

        parser.add_argument("--html-file",
                            help="outputs an html file at a given location")
        parser.add_argument("-oj", "--output-json", action="store_true",
                            help="outputs json to stdout")

        args = parser.parse_args()
        self.handle_arguments(args)

    def handle_arguments(self, arguments):
        """
            Handles the routing for arguments and the calling of main method.

            @param arguments: The parsed arguments object from argparse
        """
        html_file_path = ""
        help_messages = True
        json = False
        if arguments.api:
            inputted_api_key = input("Enter your API key:")
            if re.match("([a-zA-Z0-9]){24}", inputted_api_key):
                self.api_key = inputted_api_key
            else:
                print("Error: Please enter a valid api key")
                sys.exit(-1)

        if arguments.api_file:
            with open(arguments.api_file) as argfile:
                contents = argfile.read()
                if re.match("([a-zA-Z0-9]){24}", contents):
                    self.api_key = contents
                else:
                    print("Error: file doesn't contain a valid api key")
                    sys.exit(-1)

        if arguments.html_file:
            html_file_path = arguments.html_file

        if arguments.output_json:
            help_messages = False
            json = True

        self.main(html_file_path=html_file_path,
                  help_messages=help_messages,
                  json=json)

    def main(self, *args, **kwargs):
        """
        This brings together the etsy data and chooses the format for the
        data.
        """
        help = kwargs.get("help_messages", True)
        etsyrequest = request.Requestor(self.api_key, help)
        for code in self.CODES:
            self.listings.extend(etsyrequest.get_listings(code))
            word_processor = algorithm.Algorithm(self.listings, code)
            important_word = word_processor.process_data()
            self.word_list.append(important_word)
        html_path = kwargs.get("html_file_path", None)
        if html_path:
            out = outputformatter.HTMLOutput(self.word_list, html_path)
            out.output_html()

        if kwargs.get("json", None):
            out = outputformatter.JSONOutput(self.word_list)
            out.output_json()

if __name__ == "__main__":
    main = Main(None, None)
    main.parse_arguments()
