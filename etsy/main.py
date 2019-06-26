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
        "8595827", "1"]

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
        parser.add_argument("--api", action="store_true")
        args = parser.parse_args()
        if args.api:
            inputted_api_key = input("Enter your API key:")
            if re.match("([a-zA-Z0-9]){24}", inputted_api_key):
                self.api_key = inputted_api_key
            else:
                print("Error: Please enter a valid api key")
                sys.exit(0)

    def main(self):
        """
        This brings together the etsy data and chooses the format for the
        data.
        """
        etsyrequest = request.Requestor(3, self.api_key)
        for code in self.CODES:
            self.listings.extend(etsyrequest.get_listings(code))
            word_processor = algorithm.Algorithm(self.listings, code)
            frequency_dictionary = word_processor.process_data()
            out = outputformatter.OutputFormatter(
                frequency_dictionary, "html", "")
            self.word_list.append(frequency_dictionary)
        out = outputformatter.OutputFormatter(self.word_list, "html", "")
        out.output_html()

if __name__ == "__main__":
    a = Main("7bfab9qggezjq7gwccvwqsdb", None)
    #a.parse_arguments()
    a.main()
