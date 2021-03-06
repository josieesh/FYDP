from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from typing import Dict, Tuple

delivery_truck_weight = 8000 / 2000 # in tons

def getCoordinates(address_dict: Dict):
    geolocator = Nominatim(user_agent="FYDP")
    location = geolocator.geocode(address_dict)

    return location.latitude, location.longitude


def getDistanceMiles(source_coords: Tuple[float, float], dest_coords: Tuple[float, float]):
    return geodesic(source_coords, dest_coords).miles


def gramsToLbs(grams: float):
    return grams / 454.0


def getCarbonFootprintTruck(weight, distance):
    """
    `weight`: weight in grams
    `distance`: distances in miles

    returns the grams of CO2 emitted by an average US freight truck for the weight and distance provided.


    "average freight truck in the U.S. emits 161.8 grams of CO2 per ton-mile"
    - where "ton" is 2000 lbs
    """
    tons_package = gramsToLbs(weight) / 2000.0
    total_weight = tons_package + delivery_truck_weight
    
    ton_mile = total_weight * distance
    grams_CO2 = 161.8 * ton_mile
    return grams_CO2


def getCarbonFootprint(order):
    total_weight_grams = order.total_weight
    total_distance_miles = 0.0 # distance in miles
    if order.shipping_address is None:
        return 0.0

    for line_item in order.line_items:
        if line_item.requires_shipping:
            if line_item.origin_location is not None:
                # Get source coordinates
                address_dict = {
                    "country": line_item.origin_location["country_code"], 
                    "street": line_item.origin_location["address1"],
                    "city": line_item.origin_location["city"],
                    "postal_code":line_item.origin_location["zip"],
                }
                source_coordinates: Tuple[float, float] = getCoordinates(address_dict)
                
                # Get distance to destination
                dest_coordinates = (order.shipping_address["latitude"], order.shipping_address["longitude"])
                distance_miles = getDistanceMiles(source_coordinates, dest_coordinates)

                total_distance_miles += distance_miles
    
    if total_distance_miles != 0:
        grams_CO2 = getCarbonFootprintTruck(total_weight_grams, total_distance_miles)
        return grams_CO2

    return 0.0
                