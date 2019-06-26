from collections import Counter
from words import ShopAndWords


class Algorithm:
    """
    This class takes care of all of the data cleaning and manipulation
    in order to find the 5 most meaningful words associated with
    product listings on Etsy.

    Algorithm description:
    1. Combine all the text for every listing
    2. lowercase every item
    3. strip out all non alphanumeric characters
    4. eliminate all of the common words (e.g. the, a)
        - This step will also remove words common to selling listings
        - such as the word shipping
    5. do a frequency analysis of all words
    6. pick the five words that appear least often.
        - The least often picked word is the most meaningful due to it
        - being used the fewest amount of times.
    """

    def __init__(self, listinglist, shop_id):
        """
        @param listinglist is a list of Listing objects
        @param shop_id: the id of the Etsy shop
        @param all_text_list: the list of all words
        @param frequency_dict: the dictionary that holds word frequency data
        """
        self.listinglist = listinglist
        self.shop_id = shop_id
        self.all_text_list = []
        self.frequency_dict = {}

    def process_data(self):
        """
        Public method that does the processing.

        Calls the appropriate functions in order to process the data returned
        from the Etsy query.

        @return: ShopAndWords object that contains the shop id and the five
            most used words as a list.
        """
        self._combine_all_words()
        self._clean_data()
        return self._create_frequency_dictionary()

    def _combine_all_words(self):
        """
        Takes the information from all of the product listings
        and combines them into a giant list for processing
        """
        for productlisting in self.listinglist:
            self.all_text_list.extend(productlisting.title.lower().split())
            self.all_text_list.extend(productlisting.description.lower().split())

    def _clean_data(self):
        """
        Runs the list and all of its contents through the filtering functions
        defined below.
        """
        self.all_text_list = [self._punctuation_filter(i)
                              for i in self.all_text_list]

        self.all_text_list = [self._eliminate_common_words(i)
                              for i in self.all_text_list]

        self.all_text_list = [i for i in self.all_text_list if len(i) > 0]

    def _punctuation_filter(self, word):
        """
        This ensures that numbers and punctuation marks are removed from the
        final product.

        @param word: The string to be filtered of punctuation
        """
        returned_word = word.replace(":", "")
        returned_word = returned_word.replace("/", "")
        returned_word = returned_word.replace("0", "")
        returned_word = returned_word.replace("1", "")
        returned_word = returned_word.replace("2", "")
        returned_word = returned_word.replace("3", "")
        returned_word = returned_word.replace("4", "")
        returned_word = returned_word.replace("5", "")
        returned_word = returned_word.replace("6", "")
        returned_word = returned_word.replace("7", "")
        returned_word = returned_word.replace("8", "")
        returned_word = returned_word.replace("9", "")
        returned_word = returned_word.replace("/", "")
        returned_word = returned_word.replace("!", "")
        returned_word = returned_word.replace("?", "")
        returned_word = returned_word.replace("'", "")
        returned_word = returned_word.replace("@", "")
        returned_word = returned_word.replace(".", "")
        returned_word = returned_word.replace("(", "")
        returned_word = returned_word.replace(")", "")
        returned_word = returned_word.replace(",", "")
        returned_word = returned_word.replace("-", "")
        return returned_word

    def _eliminate_common_words(self, word):
        """
        We want to ensure that we don't put in a word such as an article
        into the meaningful words as articles are helper words.
        """
        common_words = [
            "to", "the", "and", "but", "or", "with",
            "a", "an", "shipping", "of"]
        if word in common_words:
            return ""
        return word

    def _create_frequency_dictionary(self):
        """
        Creates the frequency dictionary structured as follows:
            word : number_of_occurances

        @return a ShopAndWord object indicating the shop with its five most
                important words
        """
        self.frequency_dict = Counter(self.all_text_list)
        sorted(self.frequency_dict.values())
        important = self.frequency_dict.most_common()[:-5-1:-1]
        important_word_list = []
        for word_tuple in important:
            important_word_list.append(word_tuple[0])
        important_words = ShopAndWords(
            self.shop_id, None, important_word_list, None)
        return important_words
