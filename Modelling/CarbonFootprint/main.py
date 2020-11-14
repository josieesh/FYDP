import os
from dotenv import load_dotenv
from model import getCarbonFootprint
from shopify import getOrders



load_dotenv()


API_KEY = os.getenv("API_KEY")
API_PASSWORD = os.getenv("API_PASSWORD")
DOMAIN = os.getenv("DOMAIN")


if __name__ == "__main__":
	# Get the orders from the shop
    orders = getOrders(DOMAIN, API_KEY, API_PASSWORD)
    for order in orders:
        print(order)
        carbon_footprint = getCarbonFootprint(order)