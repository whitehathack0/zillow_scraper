import psycopg2
import requests
from celery import shared_task
from app.app import create_celery_app
import logging


celery = create_celery_app()

api_key = "215f50cb-7886-4f70-ba0e-0d69959a789a"
# zillow search url
listing_url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Boston%2C%20MA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-71.16819753363963%2C%22east%22%3A-70.98932637885447%2C%22south%22%3A42.286856959080005%2C%22north%22%3A42.39851130274666%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A400000%2C%22max%22%3A500000%7D%2C%22mp%22%3A%7B%22min%22%3A2066%2C%22max%22%3A2582%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22customRegionId%22%3A%2232cd564084X1-CR13q3s12ar2tvp_1c86do%22%7D"
url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"
querystring = {
        "api_key": api_key,
        "url": listing_url
    }


@shared_task()
def scraper():
    logging.info("Starting process...")

    logging.info("Initializing database connection...")
    conn = psycopg2.connect(host='zillow-data.czredhmlhbps.us-east-1.rds.amazonaws.com',
                            port="5432",
                            user='postgres',
                            password='umass2020',
                            database='zillow_data')
    cursor = conn.cursor()

    try:
        logging.info("Sending request...")
        res = requests.request("GET", url, params=querystring)
        res = res.json()
        logging.info("Request status: " + str(res["is_success"]))
        logging.info("Total number of houses found in search: {total}".format(
            total=str(res["data"]["categoryTotals"]["cat1"]["totalResultCount"])))

        for idx, house in enumerate(res["data"]["cat1"]["searchResults"]["listResults"]):
            logging.info("House #" + str(idx+1))

            if not (house.get('zpid') is None):
                zpid = house['zpid']
                logging.info("zpid: " + zpid)

                # Query database to see if zpid exists and if not then proceed otherwise continue
                cursor.execute("select * from zillow_data where zpid=%s", (zpid,))
                if cursor.fetchone() is not None:
                    logging.info("This ZPID already exists in DB")
                    continue
            else:
                continue

            if not (house.get('unformattedPrice') is None):
                price = house.get('unformattedPrice')
            else:
                continue

            if not (house.get('area') is None):
                area = house['area']
            else:
                continue

            if not (house.get('latLong').get('latitude') is None):
                lat = house['latLong']['latitude']
            else:
                lat = None

            if not (house.get('latLong').get('longitude') is None):
                long = house['latLong']['longitude']
            else:
                long = None

            if not (house.get('statusType') is None):
                status_type = house['statusType']
            else:
                status_type = None

            if not (house.get('zestimate') is None):
                zestimate = house['zestimate']
            else:
                zestimate = None

            if not (house.get('hdpData').get('homeInfo').get('rentZestimate') is None):
                rent_zestimate = house.get('hdpData').get('homeInfo').get('rentZestimate')
            else:
                rent_zestimate = None

            if not (house.get('hdpData').get('homeInfo').get('taxAssessedValue') is None):
                tax_assessed_value = house.get('hdpData').get('homeInfo').get('taxAssessedValue')
            else:
                tax_assessed_value = None

            if not (house.get('address') is None):
                address = house.get('address')
            else:
                address = None

            if not (house.get('detailUrl') is None):
                web_link = house.get('detailUrl')
            else:
                web_link = None

            logging.info("Inserting record...")
            cursor.execute(
                "INSERT INTO zillow_data (zpid,price,area,lat,long,statusType,zestimate,rentZestimate,taxAssessedValue, web_link, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (zpid, price, area, lat, long, status_type, zestimate, rent_zestimate, tax_assessed_value, web_link, address))
            conn.commit()
            logging.info("---")

    except Exception as e:
        logging.info("Some error occurred.....  " + str(e))
