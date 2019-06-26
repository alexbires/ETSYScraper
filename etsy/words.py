class ShopAndWords:
    """
    Represents a shop and it's five most important words.
    """

    def __init__(self, shop_id, shop_name, words_list, error):
        """
        @param shop_id: the id of the Etsy shop
        @param shop_name: the human readable Etsy shop
        @param words_list: the python list important words
        @param error: any errors that have accumulated
        """
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.words_list = words_list
        self.error = error
