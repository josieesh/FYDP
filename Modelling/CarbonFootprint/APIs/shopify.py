import json
import requests
from dataclasses import dataclass
from requests.auth import HTTPBasicAuth
from typing import Any, Dict, List, Optional



@dataclass(frozen=True)
class LineItem:
	"""
	API ressource id.
	"""
	id: int
	"""
	The service provider that's fulfilling the item. Valid values: manual, or the name of the provider, such as amazon or shipwire.
	"""
	fulfillment_service: str
	grams: int
	"""
	Whether the item requires shipping.
	"""
	requires_shipping: bool
	"""
	The location of the line item’s fulfillment origin.
		id: The location ID of the line item’s fulfillment origin. Used by Shopify to calculate applicable taxes. This is not the ID of the location where the order was placed. You can use the FulfillmentOrder resource to determine the location an item will be sourced from.
		country_code: The two-letter code (ISO 3166-1 format) for the country of the item's supplier.
		province_code: The two-letter abbreviation for the region of the item's supplier.
		name: The name of the item's supplier.
		address1: The street address of the item's supplier.
		address2: The suite number of the item's supplier.
		city: The city of the item's supplier.
		zip: The zip of the item's supplier.
		duties: A list of duty objects, each containing information about a duty on the line item.

	"""
	origin_location: Optional[Dict[str, Any]] = None
	"""
	How far along an order is in terms line items fulfilled. Valid values: null, fulfilled, partial, and not_eligible.
	"""
	fulfillment_status: Optional[str] = None
		
"""
The Order ressource from the Shopify API.
See https://shopify.dev/docs/admin-api/rest/reference/orders/order#open-2020-10 for more info.
"""
@dataclass(frozen=True)
class Order:
	"""
	API ressource id.
	"""
	id: int
	"""
	The date and time (ISO 8601 format) when the order was closed.
	E.g: "closed_at": "2008-01-10T11:00:00-05:00"
	"""
	created_at: str
	"""
	A list of line item objects, each containing information about an item in the order. Each object has the following properties:
		fulfillable_quantity: The amount available to fulfill, calculated as follows:
		quantity - max(refunded_quantity, fulfilled_quantity) - pending_fulfilled_quantity - open_fulfilled_quantity
		fulfillment_service: The service provider that's fulfilling the item. Valid values: manual, or the name of the provider, such as amazon or shipwire.
		fulfillment_status: How far along an order is in terms line items fulfilled. Valid values: null, fulfilled, partial, and not_eligible.
		grams: The weight of the item in grams.
		id: The ID of the line item.
		price: The price of the item before discounts have been applied in the shop currency.
		price_set: The price of the line item in shop and presentment currencies.
		product_id: The ID of the product that the line item belongs to. Can be null if the original product associated with the order is deleted at a later date.
		quantity: The number of items that were purchased.
		requires_shipping: Whether the item requires shipping.
		sku: The item's SKU (stock keeping unit).
		title: The title of the product.
		variant_id: The ID of the product variant.
		variant_title: The title of the product variant.
		vendor: The name of the item's supplier.
		name: The name of the product variant.
		gift_card: Whether the item is a gift card. If true, then the item is not taxed or considered for shipping charges.
		properties: An array of custom information for the item that has been added to the cart. Often used to provide product customization options. For more information, see The line_item object.
		taxable: Whether the item was taxable.
		tax_lines: A list of tax line objects, each of which details a tax applied to the item.
		title: The name of the tax.
		price: The amount added to the order for this tax in the shop currency.
		price_set: The amount added to the order for this tax in shop and presentment currencies.
		rate: The tax rate applied to the order to calculate the tax price.
		tip_payment_gateway: The payment gateway used to tender the tip, such as shopify_payments. Present only on tips.
		tip_payment_method: The payment method used to tender the tip, such as Visa. Present only on tips.
		total_discount: The total amount of the discount allocated to the line item in the shop currency. This field must be explictly set using draft orders, Shopify scripts, or the API. Instead of using this field, Shopify recommends using discount_allocations, which provides the same information.
		total_discount_set: The total amount allocated to the line item in the presentment currency. Instead of using this field, Shopify recommends using discount_allocations, which provides the same information.
		discount_allocations: An ordered list of amounts allocated by discount applications. Each discount allocation is associated to a particular discount application.
		amount: The discount amount allocated to the line in the shop currency.
		discount_application_index: The index of the associated discount application in the order's discount_applications list.
		amount_set: The discount amount allocated to the line item in shop and presentment currencies.
		origin_location: The location of the line item’s fulfillment origin.
		id: The location ID of the line item’s fulfillment origin. Used by Shopify to calculate applicable taxes. This is not the ID of the location where the order was placed. You can use the FulfillmentOrder resource to determine the location an item will be sourced from.
		country_code: The two-letter code (ISO 3166-1 format) for the country of the item's supplier.
		province_code: The two-letter abbreviation for the region of the item's supplier.
		name: The name of the item's supplier.
		address1: The street address of the item's supplier.
		address2: The suite number of the item's supplier.
		city: The city of the item's supplier.
		zip: The zip of the item's supplier.
		duties: A list of duty objects, each containing information about a duty on the line item.
	"""
	line_items: List[LineItem]
	"""
	An array of objects, each of which details a shipping method used. Each object has the following properties:
		code: A reference to the shipping method.
		discounted_price: The price of the shipping method after line-level discounts have been applied. Doesn't reflect cart-level or order-level discounts.
		discounted_price_set: The price of the shipping method in both shop and presentment currencies after line-level discounts have been applied.
		price: The price of this shipping method in the shop currency. Can't be negative.
		price_set: The price of the shipping method in shop and presentment currencies.
		source: The source of the shipping method.
		title: The title of the shipping method.
		tax_lines: A list of tax line objects, each of which details a tax applicable to this shipping line.
		carrier_identifier: A reference to the carrier service that provided the rate. Present when the rate was computed by a third-party carrier service.
		requested_fulfillment_service_id: A reference to the fulfillment service that is being requested for the shipping method. Present if the shipping method requires processing by a third party fulfillment service; null otherwise.

		Eg:
		"shipping_lines": [
			{
				"code": "INT.TP",
				"price": "4.00",
				"discounted_price": "4.00",
				"price_set": {...},
				"discounted_price_set": {...},
				"source": "canada_post",
				"title": "Small Packet International Air",
				"tax_lines": [],
				"carrier_identifier": "third_party_carrier_identifier",
				"requested_fulfillment_service_id": "third_party_fulfillment_service_id"
			}
		]
	"""
	shipping_lines: List[Dict[str, Any]]
	"""
	Whether this is a test order (true/false)
	"""
	test: bool
	"""
	The sum of all line item weights in grams.
	"""
	total_weight: int
	"""
	The date and time ( ISO 8601 format) when the order was canceled.
	"cancelled_at": null
	"""
	cancelled_at: Optional[str] = None
	customer: Optional[Dict[str, Any]] = None
	"""
	The mailing address to where the order will be shipped. This address is optional and will not be available on orders that do not require shipping
	"shipping_address": {
		"address1": "123 Amoebobacterieae St",
		"address2": "",
		"city": "Ottawa",
		"company": null,
		"country": "Canada",
		"first_name": "Bob",
		"last_name": "Bobsen",
		"latitude": "45.41634",
		"longitude": "-75.6868",
		"phone": "555-625-1199",
		"province": "Ontario",
		"zip": "K2P0V6",
		"name": "Bob Bobsen",
		"country_code": "CA",
		"province_code": "ON"
	}
	"""
	shipping_address: Optional[str] = None


def createLineItemObject(line_item_dict):
	final_dict = {}
	for field_of_interest in LineItem.__dataclass_fields__.keys():
		if field_of_interest in line_item_dict:
			final_dict[field_of_interest] = line_item_dict[field_of_interest]
	
	return final_dict


def createOrderObject(order_dict):
	final_dict = {}
	for field_name, _ in Order.__dataclass_fields__.items():
		if field_name in order_dict: # Some values can be null, and thus would not be sent back in the response.
			if field_name == "line_items":
				line_items = []
				for line_item_dict in order_dict["line_items"]:
					line_items.append(LineItem(**createLineItemObject(line_item_dict)))
				
				final_dict["line_items"] = line_items
			else:
				final_dict[field_name] = order_dict[field_name]

	return Order(**final_dict)


def getOrders(domain, api_key, api_password):
	url = f"https://{domain}/admin/api/2020-10/orders.json"    
	auth = HTTPBasicAuth(api_key, api_password)
	r = requests.get(url, auth=auth)

	# Parse the response
	json_result: Dict[str, str] = json.loads(r.text)
	orders: List[Order] = []
	for order_dict in json_result["orders"]:
		orders.append(createOrderObject(order_dict))

	return orders


def getFulfillment(domain, api_key, api_password, order_id):
	"""
	GET /admin/api/2020-10/orders/{order_id}/fulfillments.json
	Retrieves fulfillments associated with an order
	"""

	url = f"https://{domain}/admin/api/2020-10/orders/{order_id}/fulfillments.json"
	auth = HTTPBasicAuth(api_key, api_password)
	r = requests.get(url, auth=auth)
	json_result: Dict[str, str] = json.loads(r.text)
	print(json_result)
