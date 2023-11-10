import json
import pickle
from os import path

parent_dir = path.dirname(path.abspath(__file__))

def update_price(product, price_info):
    method = price_info['method']
    match method:
        case "add":
            product['price'] = product['price'] + price_info['param']
        case "sub":
            product['price'] = product['price'] - price_info['param']
        case "percent+":
            product['price'] = product['price'] * (1 + price_info["param"])
        case "percent-":
            product['price'] = product['price'] * (1 - price_info["param"])

    product["price"] = round(product["price"], 2)

with open(path.join(parent_dir, 'data', 'price_info_71.json')) as file:
    price_info = json.load(file)

with open(path.join(parent_dir, 'data', 'products_71.pkl'), "rb") as file:
    products = pickle.load(file)

price_product_info = {}

for item in price_info:
    price_product_info[item['name']] = item
for product in products:
    current_product = price_product_info[product['name']]
    update_price(product, current_product)

with open(path.join(parent_dir, 'result', '4', 'update_price_products.pkl'), 'wb') as result:
    result.write(pickle.dumps(products))