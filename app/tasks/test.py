import celery
import requests
import psycopg2
import re


class DB:

    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn:
            self.conn.close()

        self.conn = psycopg2.connect(host='zillow-data.czredhmlhbps.us-east-1.rds.amazonaws.com',
                                     port="5432",
                                     user='postgres',
                                     password='umass2020',
                                     database='zillow_data')

    def query(self, postgres_insert_query, record_to_insert):
        try:
            cursor = self.conn.cursor()
            cursor.execute(postgres_insert_query, record_to_insert)
            self.conn.commit()
            count = cursor.rowcount
            print(count, "Record successfully queried into zillow_data table")
            return cursor

        except (AttributeError, psycopg2.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(postgres_insert_query, record_to_insert)
            self.conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
            return cursor

        # finally:
        #     if self.conn:
        #         cursor.close()
        #         self.conn.close()
        #     print("PostgreSQL connection is closed")

        return cursor


api_key = "215f50cb-7886-4f70-ba0e-0d69959a789a"

database = DB()

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

    # database.connect()

    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    logger.info("Sending request...")
    try:
        res = requests.request("GET", url, params=querystring)
        logger.info("Request status: " + str(res.json()["is_success"]))
        logger.info("Total number of houses found in search: {total}".format(
            total=str(res.json()["data"]["categoryTotals"]["cat1"]["totalResultCount"])))

        for house in res.json()["data"]["cat1"]["searchResults"]["mapResults"]:
            if not (house.get('zpid') is None):
                # Query databse to see if zpid exists and if not then proceed otherwise continue
                zpid = house['zpid']
                postgreSQL_select_Query = "select * from zillow_data where zpid=%s"
                cursor = database.query(postgreSQL_select_Query, (int(zpid),))
                if len(cursor.fetchall()) > 0:
                    continue
            else:
                continue

            if not (house.get('price') is None):
                price = house['price']
                print(price)
                pattern = '\$.*'
                price = re.search(pattern, price).group()
            else:
                continue
                price = None

            if not (house.get('area') is None):
                area = house['area']
            else:
                continue
                area = None

            if not (house.get('latLong').get('latitude') is None):
                lat = house['latLong']['latitude']
            else:
                lat = None

            if not (house.get('latLong').get('longitude') is None):
                long = house['latLong']['longitude']
            else:
                long = None

            if not (house.get('statusType') is None):
                statusType = house['statusType']
            else:
                statusType = None

            if not (house.get('zestimate') is None):
                zestimate = house['zestimate']
            else:
                zestimate = None

            if not (house.get('rentZestimate') is None):
                rentZestimate = house['rentZestimate']
            else:
                rentZestimate = None

            if not (house.get('taxAssessedValue') is None):
                taxAssessedValue = house['taxAssessedValue']
            else:
                taxAssessedValue = None

            postgres_insert_query = "INSERT INTO zillow_data (zpid,price,area,lat,long,statusType,zestimate,rentZestimate,taxAssessedValue) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            record_to_insert = (zpid, price, area, lat, long, statusType, zestimate, rentZestimate, taxAssessedValue)
            database.query(postgres_insert_query, record_to_insert)

    except Exception as e:
        logger.info("Some error occurred lol....." + str(e))
