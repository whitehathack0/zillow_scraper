import celery
import requests

api_key = "215f50cb-7886-4f70-ba0e-0d69959a789a"

# zillow search url
listing_url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Boston%2C%20MA" \
              "%22%2C%22mapBounds%22%3A%7B%22west%22%3A-71.16819753363963%2C%22east%22%3A-70.98932637885447%2C" \
              "%22south%22%3A42.286856959080005%2C%22north%22%3A42.39851130274666%7D%2C%22isMapVisible%22%3Atrue%2C" \
              "%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B" \
              "%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A400000%2C%22max%22%3A500000%7D%2C%22mp%22%3A%7B" \
              "%22min%22%3A2066%2C%22max%22%3A2582%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B" \
              "%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse" \
              "%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22customRegionId%22%3A%2232cd564084X1" \
              "-CR13q3s12ar2tvp_1c86do%22%7D"


@celery.task()
def print_hello():
    logger = print_hello.get_logger()

    logger.info("Starting process...")

    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    logger.info("Sending request...")
    try:
        res = requests.request("GET", url, params=querystring)
        logger.info("Request status: " + str(res.json()["is_success"]))
        logger.info("Total number of houses found in search: {total}".format(total=str(res.json()["data"]["categoryTotals"]["cat1"]["totalResultCount"])))

        i = 0
        for house in res.json()["data"]["cat1"]["searchResults"]["mapResults"]:
            print(house)
            i += 1
            if i == 1:
                break;

    except Exception:
        logger.info("Some error occured lol.....")
