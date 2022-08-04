from csv import excel
import math
import pandas as pd
from typing import List
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

class StandardProduct:
    stock_code = ""
    brand_name = ""
    category = ""
    description = ""
    cost = 0.0
    wastage =  0.0
    uom_amount = 0.0
    uom_unit = ""
    uom_packaging_type = ""
    def __init__(self, stock_code, brand_name, category, description, cost, wastage, uom_amount, uom_unit, uom_packaging_type):
        self.stock_code = stock_code
        self.brand_name = brand_name
        self.category = category
        self.description = description
        self.cost = cost
        self.wastage = wastage
        self.uom_amount = uom_amount
        self.uom_unit = uom_unit
        self.uom_packaging_type = uom_packaging_type

    def __str__ (self):
        return """StandardProduct(
    stock_code={stock_code}, 
    brand_name={brand_name}, 
    category={category}, 
    description={description}, 
    cost={cost}, 
    wastage={wastage}, 
    uom_amount={uom_amount}, 
    uom_unit={uom_unit}, 
    uom_packaging_type={uom_packaging_type}
)
        """.format(
            stock_code=self.stock_code, 
            brand_name=self.brand_name, 
            category=self.category,
            description=self.description,
            cost=self.cost,
            wastage=self.wastage,
            uom_amount=self.uom_amount,
            uom_unit=self.uom_unit,
            uom_packaging_type=self.uom_packaging_type,
        )


excel_file = pd.read_excel("files/ExcelTemplate.xlsx", skiprows=12, usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14])
print(excel_file)
products:List[StandardProduct] = []
for index, row in excel_file.iterrows():
    stock_code = row[0]
    brand_name = row[1]
    category = row[2]
    description = row[3]
    cost = row[4]
    wastage =  row[5]
    uom_amount = row[6]
    uom_unit = row[7]
    uom_packaging_type = row[8]
    product = StandardProduct(
        stock_code = stock_code if isinstance(stock_code, str) else "",
        brand_name = brand_name if isinstance(brand_name, str) else "",
        category = category if isinstance(category, str) else "",
        description = description if isinstance(description, str) else "",
        cost = cost if isinstance(cost, float) or isinstance(cost, int) else float(0.0),
        wastage = wastage if isinstance(wastage, float) or isinstance(wastage, int) else float(0.0),
        uom_amount = uom_amount if isinstance(uom_amount, float) or isinstance(uom_amount, int) else float(0.0),
        uom_unit = uom_unit if isinstance(uom_unit, str) else "",
        uom_packaging_type = uom_packaging_type if isinstance(uom_packaging_type, str) else "",
    )
    # product = {
    #     "stock_code": stock_code if isinstance(stock_code, str) else "",
    #     "brand_name": brand_name if isinstance(brand_name, str) else "",
    #     "category": category if isinstance(category, str) else "",
    #     "description": description if isinstance(description, str) else "",
    #     "cost": cost if isinstance(cost, float) or isinstance(cost, int) else float(0.0),
    #     "wastage": wastage if isinstance(wastage, float) or isinstance(wastage, int) else float(0.0),
    #     "uom_amount": uom_amount if isinstance(uom_amount, float) or isinstance(uom_amount, int) else float(0.0),
    #     "uom_unit": uom_unit if isinstance(uom_unit, str) else "",
    #     "uom_packaging_type": uom_packaging_type if isinstance(uom_packaging_type, str) else "",
    # }
    products.append(product)


# Import to Saleor
etl_data_loader = ETLDataLoader("U80jcOkX2xlCF306YJTiMZxW1R8Tn8")
warehouse_id = "V2FyZWhvdXNlOjVlYTEwZTliLWFjMTEtNDMxYS04M2IxLWE5ZmMyM2NjZmNhZQ=="

# create brand name attribute used as variant:
print("========== CREATE ATTRIBUTE: Stock code ==========")
stock_code_attribute_id =  etl_data_loader.create_attribute(name="Stock code", inputType="RICH_TEXT", slug="attribute-stock-code")
print("stock_code_attribute_id = " + stock_code_attribute_id)
stock_code_attribute_id = "QXR0cmlidXRlOjEy"

# create brand name attribute used as variant:
print("========== CREATE ATTRIBUTE: Brand name ==========")
brand_name_attribute_id =  etl_data_loader.create_attribute(name="Brand name", inputType="RICH_TEXT", slug="attribute-brand-name")
print("brand_name_attribute_id = " + brand_name_attribute_id)
brand_name_attribute_id = "QXR0cmlidXRlOjc="

# create wastage attribute used as variant:
print("========== CREATE ATTRIBUTE: Wastage Percentage ==========")
wastage_percentage_attribute_id =  etl_data_loader.create_attribute(name="Wastage Percentage", inputType="NUMERIC", slug="attribute-wastage-percentage")
print("wastage_percentage_attribute_id = " + wastage_percentage_attribute_id)
wastage_percentage_attribute_id = "QXR0cmlidXRlOjg="

# Create stock measurement amount attribute used as variant:
print("========== CREATE ATTRIBUTE: Stock Measurement - Amount ==========")
stock_measurement_amount_attribute_id =  etl_data_loader.create_attribute(name="Stock Measurement - Amount", inputType="NUMERIC", slug="attribute-stock-measurement-amount")
print("stock_measurement_amount_attribute_id = " + stock_measurement_amount_attribute_id)
stock_measurement_amount_attribute_id = "QXR0cmlidXRlOjk="

# Create stock measurement unit attribute used as variant:
print("========== CREATE ATTRIBUTE: Stock Measurement - Unit ==========")
stock_measurement_unit_attribute_id =  etl_data_loader.create_attribute(name="Stock Measurement - Unit", inputType="RICH_TEXT", slug="attribute-stock-measurement-unit")
print("stock_measurement_unit_attribute_id = " + stock_measurement_unit_attribute_id)
stock_measurement_unit_attribute_id = "QXR0cmlidXRlOjEw"

# Create stock measurement packaging type attribute used as variant:
print("========== CREATE ATTRIBUTE: Stock Measurement - Packaging Type ==========")
stock_measurement_packaging_type_attribute_id =  etl_data_loader.create_attribute(name="Stock Measurement - Packaging Type", inputType="RICH_TEXT", slug="attribute-stock-measurement-packaging-type")
print("stock_measurement_packaging_type_attribute_id = " + stock_measurement_packaging_type_attribute_id)
stock_measurement_packaging_type_attribute_id = "QXR0cmlidXRlOjEx"

# create a product type: standard
print("========== CREATE PRODUCT TYPE: standard ==========")
product_type_id = etl_data_loader.create_product_type(name="standard",
                                                      hasVariants=True, 
                                                      slug="product-type-standard",
                                                      productAttributes=[],
                                                      variantAttributes=[
                                                        stock_code_attribute_id,
                                                        brand_name_attribute_id, 
                                                        wastage_percentage_attribute_id, 
                                                        stock_measurement_amount_attribute_id, 
                                                        stock_measurement_unit_attribute_id, 
                                                        stock_measurement_packaging_type_attribute_id
                                                    ])
print("product_type_id = " + product_type_id)
product_type_id = "UHJvZHVjdFR5cGU6NA=="

# create categories
print("========== CREATE CATEGORIES ==========")
unique_categories = set([product.category for product in products])
print(unique_categories)

cat_to_id = {}
for category in unique_categories:
    cat_to_id[category] = etl_data_loader.create_category(name=category, 
                                                          slug="category-" + category.replace(" ", "-").lower()
                                                        )
print(cat_to_id)
cat_to_id = {'Equipment': 'Q2F0ZWdvcnk6Mw==', 'General': 'Q2F0ZWdvcnk6NA==', 'Frozen': 'Q2F0ZWdvcnk6NQ==', 'Consumables - bar': 'Q2F0ZWdvcnk6Ng==', 'Coolroom': 'Q2F0ZWdvcnk6Nw==', 'Drygoods': 'Q2F0ZWdvcnk6OA==', 'Chemicals': 'Q2F0ZWdvcnk6OQ=='}

print("========== CREATE PRODUCTS ==========")
for product in products:
    description_json = dummy_editorjs(product.description, json_format=True)
    print("description_json = " + description_json)
    if len(product.stock_code) > 0:
        product_id = etl_data_loader.create_product(product_type_id,
                                                    name=product.description,
                                                    description=description_json,
                                                    slug=product.stock_code.strip(),
                                                    # basePrice=product["price"],
                                                    # sku=product["sku"],
                                                    category=cat_to_id[product.category],
                                                    attributes=[
                                                        # {"id": stock_code_attribute_id, "richText": product.stock_code},
                                                        # {"id": brand_name_attribute_id, "values": [product.brand_name]},
                                                        # {"id": wastage_percentage_attribute_id, "values": [product.wastage]},
                                                        # {"id": stock_measurement_amount_attribute_id, "values": [product.uom_amount]},
                                                        # {"id": stock_measurement_unit_attribute_id, "values": [product.uom_unit]},
                                                        # {"id": stock_measurement_packaging_type_attribute_id, "values": [product.uom_packaging_type]}
                                                    ],
                                                    # isPublished=True
                                                    )
        print("product_id (new) = " + product_id)
        if len(product_id) == 0:
            # Get product ID by query
            productsByName = etl_data_loader.get_products(product.description.replace("-", " "))
            print("productsByName: " + product.description)
            print(productsByName)
            if len(productsByName["edges"]) > 0:
                foundProduct = productsByName["edges"][0]
                product_id = foundProduct["node"]["id"]
                print("product_id (existing) = " + product_id)
        variant_id = etl_data_loader.create_product_variant(product_id,
                                                            sku=product.stock_code,
                                                            attributes=[
                                                                {"id": stock_code_attribute_id, "richText": dummy_editorjs(product.stock_code, json_format=True)},
                                                                {"id": brand_name_attribute_id, "richText": dummy_editorjs(product.brand_name, json_format=True)},
                                                                {"id": wastage_percentage_attribute_id, "values": [str(product.wastage)]},
                                                                {"id": stock_measurement_amount_attribute_id, "values": [str(product.uom_amount)]},
                                                                {"id": stock_measurement_unit_attribute_id, "richText": dummy_editorjs(product.uom_unit, json_format=True)},
                                                                {"id": stock_measurement_packaging_type_attribute_id, "richText": dummy_editorjs(product.uom_packaging_type, json_format=True)}
                                                            ],
                                                            # costPrice=product["price"],
                                                            weight=0.75,
                                                            stocks=[
                                                                {"warehouse": warehouse_id, "quantity": 15}
                                                            ])
        print("variant_id = " + variant_id)
        # break
        # variant_id = "UHJvZHVjdFZhcmlhbnQ6MTE="
        # break # Test one product first