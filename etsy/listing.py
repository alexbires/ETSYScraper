class Listing:
    """
    Represents a listing on Etsy.
    """

    def __init__(self, title, description, shop_id):
        """
        @param title: The title of the listing
        @param description: The listing's description
        @param shop_id: The id of the shop as defined by the Etsy API
        """
        self.title = title
        self.description = description
        self.shop_id = shop_id

    def str(self):
        return "Title:" + self.title
