from dotenv import load_dotenv
import os
from rich.console import Console
from helper import call_api
import pprint

console = Console()

load_dotenv()

# Get the Grocy API URL and Bearer token from the environment
grocy_url = os.environ['GROCY_HOST']
token = os.environ['GROCY_TOKEN']

console.rule("Add missing items to Shopping List")

print(call_api(f"{grocy_url}/api/stock/shoppinglist/add-missing-products", grocy_api_key=token, query_type='POST', body={})) # ohne dem leeren Body 500 Error

console.rule("Remove done Items")

print(call_api(f"{grocy_url}/api/stock/shoppinglist/clear", grocy_api_key=token, query_type='POST', body={"done_only": True}))

console.rule("Get Items from Shopping List")

items = call_api(f"{grocy_url}/api/objects/shopping_list", grocy_api_key=token, query_type="GET")

pprint.pprint(items)

console.rule("Get Product Names")

for item in items:
    product = call_api(f"{grocy_url}/api/stock/products/{item['product_id']}", grocy_api_key=token, query_type="GET")
    print(f"{product['product']['name']} - Amount: {item['amount']}")