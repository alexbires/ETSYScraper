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

    def __init__(self, retries, api_key):
        """
        @param retries: the number of retries to in case of failure
        @param api_key: the api key for Etsy
        """
        self.retries = retries
        self.api_key = api_key

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

        request = requests.get(url)
        try:
            if request.status_code == 200:
                response = request.json()
                listinglist = []

                for listings in response["results"]:
                    product_listing = listing.Listing(
                        listings["title"],
                        listings["description"],
                        shop_id)
                    listinglist.append(product_listing)
                return listinglist

            elif request.status_code == 404:
                return [listing.Listing("", "", "ShopId does not exist")]

        except JSONDecodeError:
            return [listing.Listing("", "", "ShopId does not exist")]
