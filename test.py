from saleor_gql_loader import ETLDataLoader
from base64 import b64encode as _base64, b64decode as _unbase64
import sys
import json

def to_global_id(type, id):
    """
    Takes a type name and an ID specific to that type name, and returns a
    "global ID" that is unique among all types.
    """
    return base64(':'.join([type, text_type(id)]))

def base64(s):
    return _base64(s.encode('utf-8')).decode('utf-8')

def dummy_editorjs(text, json_format=False):
    data = {"blocks": [{"data": {"text": text}, "type": "paragraph"}]}
    return json.dumps(data) if json_format else data

# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)

if PY3:
    text_type = str
else:
    text_type = unicode

etl_data_loader = ETLDataLoader("U80jcOkX2xlCF306YJTiMZxW1R8Tn8")

# create a default warehouse
create_warehouse_wargs = {
    "slug": "example-warehouse",
    "email": "test@example.com",
    "name": "Example Warehouse",
    "address": {
        "firstName": "",
        "lastName": "",
        "companyName": "",
        "streetAddress1": "An example warehouse address",
        "streetAddress2": "",
        "city": "Melbourne",
        "cityArea": "Yarraville",
        "postalCode": "3777",
        "country": "AU",
        "countryArea": "Victoria",
        "phone": "03 3777 5777"
    }
}
# warehouse_id = etl_data_loader.create_warehouse(**create_warehouse_wargs)
# print(warehouse_id)
# V2FyZWhvdXNlOjVlYTEwZTliLWFjMTEtNDMxYS04M2IxLWE5ZmMyM2NjZmNhZQ==
warehouse_id = "V2FyZWhvdXNlOjVlYTEwZTliLWFjMTEtNDMxYS04M2IxLWE5ZmMyM2NjZmNhZQ=="

list_warehouses = etl_data_loader.list_warehouses()
print(list_warehouses)
# print(to_global_id("Warehouse", "5ea10e9b-ac11-431a-83b1-a9fc23ccfcae"));
# print("V2FyZWhvdXNlOjVlYTEwZTliLWFjMTEtNDMxYS04M2IxLWE5ZmMyM2NjZmNhZQ==");

create_shipping_zone_wargs = {
    "name": "Example shipping zone",
    "description": "This is an example shipping zone",
    "countries": ["AU"],
    "default": False,
    "addWarehouses": [warehouse_id],
    # "addWarehouses": [to_global_id("Warehouse", "5ea10e9b-ac11-431a-83b1-a9fc23ccfcae")],
    "addChannels": []
}
# shipping_zone_id = etl_data_loader.create_shipping_zone(**create_shipping_zone_wargs)
# print(shipping_zone_id)
# U2hpcHBpbmdab25lOjE=

products = [
    {
        "name": "tea a",
        "description": "description for tea a",
        "category": "green tea",
        "price": 5.5,
        "strength": "medium"
    },
    {
        "name": "tea b",
        "description": "description for tea b",
        "category": "black tea",
        "price": 10.5,
        "strength": "strong"
    },
    {
        "name": "tea c",
        "description": "description for tea c",
        "category": "green tea",
        "price": 9.5,
        "strength": "light"
    }
]

# add basic sku to products
for i, product in enumerate(products):
    product["sku"] = "{:05}-00".format(i+1)

print("List of products:")
print(products)

# create the strength attribute
# print("========== CREATE ATTRIBUTE: strength ==========")
#strength_attribute_id = etl_data_loader.create_attribute(name="strength")
#print("strength_attribute_id = " + strength_attribute_id)
strength_attribute_id = "QXR0cmlidXRlOjE="

# print("========== CREATE ATTRIBUTE VALUES FOR ATTRIBUTE: strength ==========")
# unique_strength = set([product['strength'] for product in products])
# for strength in unique_strength:
#     etl_data_loader.create_attribute_value(strength_attribute_id, name=strength)

# create another quantity attribute used as variant:
# print("========== CREATE ATTRIBUTE: qty ==========")
# qty_attribute_id =  etl_data_loader.create_attribute(name="qty")
# print("qty_attribute_id = " + qty_attribute_id)
qty_attribute_id = "QXR0cmlidXRlOjI="

# print("========== CREATE ATTRIBUTE VALUES FOR ATTRIBUTE: qty ==========")
unique_qty = {"100g", "200g", "300g"}
# for qty in unique_qty:
#     etl_data_loader.create_attribute_value(qty_attribute_id, name=qty)

# create a product type: tea
# print("========== CREATE PRODUCT TYPE: tea ==========")
# product_type_id = etl_data_loader.create_product_type(name="tea",
#                                                       hasVariants=True, 
#                                                       productAttributes=[strength_attribute_id],
#                                                       variantAttributes=[qty_attribute_id])
# print("product_type_id = " + product_type_id)
product_type_id = "UHJvZHVjdFR5cGU6MQ=="

# create categories
# print("========== CREATE CATEGORIES ==========")
# unique_categories = set([product['category'] for product in products])

# cat_to_id = {}
# for category in unique_categories:
#     cat_to_id[category] = etl_data_loader.create_category(name=category)

# print("cat_to_id:")
# print(cat_to_id)
cat_to_id = {"black tea": "Q2F0ZWdvcnk6MQ==", "green tea": "Q2F0ZWdvcnk6Mg=="}

# create products and store id
# print("========== CREATE PRODUCTS ==========")
# for i, product in enumerate(products):
#     description_json = dummy_editorjs(product["description"], json_format=True)
#     print("description_json = " + description_json)
#     product_id = etl_data_loader.create_product(product_type_id,
#                                                 name=product["name"],
#                                                 description=description_json,
#                                                 # slug=product["name"],
#                                                 # basePrice=product["price"],
#                                                 # sku=product["sku"],
#                                                 category=cat_to_id[product["category"]],
#                                                 attributes=[{"id": strength_attribute_id, "values": [product["strength"]]}],
#                                                 # isPublished=True
#                                                 )
#     products[i]["id"] = product_id

# print("List of products (after created):")
# print(products)
products = [
    {
        'name': 'tea a', 
        'description': 'description for tea a', 
        'category': 'green tea', 
        'price': 5.5, 
        'strength': 'medium', 
        'sku': '00001-00', 
        'id': 'UHJvZHVjdDox',
        'variants': []
    }, 
    {
        'name': 'tea b', 
        'description': 'description for tea b', 
        'category': 'black tea', 
        'price': 10.5, 
        'strength': 'strong', 
        'sku': '00002-00', 
        'id': 'UHJvZHVjdDoy',
        'variants': []
    }, 
    {
        'name': 'tea c', 
        'description': 'description for tea c', 
        'category': 'green tea', 
        'price': 9.5, 
        'strength': 'light', 
        'sku': '00003-00', 
        'id': 'UHJvZHVjdDoz',
        'variants': []
    }
]

# create some variant for each product:
# print("========== CREATE PRODUCT VARIANTS ==========")
# for product in products:
#     for i, qty in enumerate(unique_qty):
#         variant_id = etl_data_loader.create_product_variant(product["id"],
#                                                             sku=product["sku"].replace("-00", "-1{}".format(i+1)),
#                                                             attributes=[{"id": qty_attribute_id, "values": [qty]}],
#                                                             # costPrice=product["price"],
#                                                             weight=0.75,
#                                                             stocks=[{"warehouse": warehouse_id, "quantity": 15}])
#         product["variants"].append({
#             'id' : variant_id
#         })

# print("List of product with variants (after created variants):")
# print(products)

products = [{
	'name': 'tea a',
	'description': 'description for tea a',
	'category': 'green tea',
	'price': 5.5,
	'strength': 'medium',
	'sku': '00001-00',
	'id': 'UHJvZHVjdDox',
	'variants': [{
		'id': 'UHJvZHVjdFZhcmlhbnQ6Mg=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6Mw=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6NA=='
	}]
}, {
	'name': 'tea b',
	'description': 'description for tea b',
	'category': 'black tea',
	'price': 10.5,
	'strength': 'strong',
	'sku': '00002-00',
	'id': 'UHJvZHVjdDoy',
	'variants': [{
		'id': 'UHJvZHVjdFZhcmlhbnQ6NQ=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6Ng=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6Nw=='
	}]
}, {
	'name': 'tea c',
	'description': 'description for tea c',
	'category': 'green tea',
	'price': 9.5,
	'strength': 'light',
	'sku': '00003-00',
	'id': 'UHJvZHVjdDoz',
	'variants': [{
		'id': 'UHJvZHVjdFZhcmlhbnQ6OA=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6OQ=='
	}, {
		'id': 'UHJvZHVjdFZhcmlhbnQ6MTA='
	}]
}]