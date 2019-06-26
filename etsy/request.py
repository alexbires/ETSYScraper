import sys
from json import JSONDecodeError
import requests
import listing


class Requestor:
    """
    This class is responsible for handling all of the communicaiton with the
    Etsy service and returning data in the form of a listing object.
    """

    # the GET api path for getting shop listings
    # the inner {} represents the shop id
    GET_SHOP_LISTINGS = "/v2/shops/{}/listings/active"
    ETSY_API_URL = "https://openapi.etsy.com"
    API_PARAM = "?api_key={}"

    def __init__(self, api_key, help_messages):
        """
        @param api_key: the api key for Etsy
        @param help_messages: boolean for if help messsages should be
            printed to the screen.  If this program is being used in
            a pipeline and used for it's json it shouldn't print out any
            helpful messages.
        """

        self.api_key = api_key
        self.help_messages = help_messages

    def get_listings(self, shop_id):
        """
        This method allows us to get all of the active listings given
        a shop_id

        @param shop_id: the id of the Etsy shop
        @return: a list of Listings
        """
        url = self.ETSY_API_URL
        url += self.GET_SHOP_LISTINGS.format(shop_id)
        url += self.API_PARAM.format(self.api_key)

        response = requests.get(url)
        try:
            if response.status_code == 403:
                error = "Error: request is not authenticated please"
                error += " enter a valid API key and try again"
                print(error)
                sys.exit(-1)

            elif  response.headers["X-RateLimit-Remaining"] == 0:
                error = "Your rate limit is surpassed please try again "
                error += "in a number of hours"
                print(error)
                sys.exit(-1)

            elif response.status_code == 404:
                return [listing.Listing("", "", "ShopId does not exist")]

            elif response.status_code == 200:
                self.print_help("Shop id {}'s codes were fetched successfully"
                                .format(shop_id))

                response_json = response.json()
                listing_list = []

                for listings in response_json["results"]:
                    product_listing = listing.Listing(
                        listings["title"],
                        listings["description"],
                        shop_id)

                    listing_list.append(product_listing)

                return listing_list

        except JSONDecodeError:
            return [listing.Listing("", "", "ShopId does not exist")]

    def print_help(self, help_message):
        """
        Prints a helpful message to the screen if help messages are turned on.
        Will be turned off in the case we are outputting json as if used in a
        linux process pipeline
        """
        if self.help_messages:
            print(help_message)
