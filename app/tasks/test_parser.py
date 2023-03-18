import json


def print_hello():
    # log = print_hello.get_log()

    print("Starting process...")

    with open('../../sample.json') as sample:
        res = json.load(sample)

        print("Request status: " + str(res["is_success"]))
        print("Total number of houses found in search: {total}".format(
            total=str(res["data"]["categoryTotals"]["cat1"]["totalResultCount"])))

        for idx, house in enumerate(res["data"]["cat1"]["searchResults"]["listResults"]):
            print("House number " + str(idx))
            # print(house)
            if not (house.get('zpid') is None):
                # Query databse to see if zpid exists and if not then proceed otherwise continue
                zpid = house['zpid']
                print(zpid)
            else:
                print("zpid DNE")
                continue

            if not (house.get('unformattedPrice') is None):
                price = house.get('unformattedPrice')
                print(price)
                # pattern = '\$.*'
                # price = re.search(pattern, price).group()
            else:
                print("Price DNE")
                continue

            if not (house.get('area') is None):
                area = house['area']
                print(area)
            else:
                print("Area DNE")
                continue

            if not (house.get('latLong').get('latitude') is None):
                lat = house['latLong']['latitude']
                print(lat)
            else:
                print("Lat DNE")
                lat = None

            if not (house.get('latLong').get('longitude') is None):
                long = house['latLong']['longitude']
                print(long)
            else:
                print("Long DNE")
                long = None

            if not (house.get('statusType') is None):
                statusType = house['statusType']
                print(statusType)
            else:
                print("Status Type DNE")
                statusType = None

            if not (house.get('zestimate') is None):
                zestimate = house['zestimate']
                print(zestimate)
            else:
                print("Zestimate DNE")
                zestimate = None

            if not (house.get('hdpData').get('homeInfo').get('rentZestimate') is None):
                rentZestimate = house.get('hdpData').get('homeInfo').get('rentZestimate')
                print(rentZestimate)
            else:
                print("Rent Zestimate DNE")
                rentZestimate = None

            if not (house.get('hdpData').get('homeInfo').get('taxAssessedValue') is None):
                taxAssessedValue = house.get('hdpData').get('homeInfo').get('taxAssessedValue')
                print(taxAssessedValue)
            else:
                print("Tax Assessed Value DNE")
                taxAssessedValue = None

            print()

            # postgres_insert_query = "INSERT INTO zillow_data (zpid,price,area,lat,long,statusType,zestimate,rentZestimate,taxAssessedValue) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # record_to_insert = (zpid, price, area, lat, long, statusType, zestimate, rentZestimate, taxAssessedValue)
            # database.query(postgres_insert_query, record_to_insert)


if __name__ == "__main__":
    print_hello()
