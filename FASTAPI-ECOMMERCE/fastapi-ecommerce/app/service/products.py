import json
from pathlib import Path
from typing import Dict, List
from schema.product import Product

DATA_FILE=Path(__file__).parent.parent/"data"/"dummy.json"
def load_products()->List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,"r",encoding="utf-8") as file:
        return json.load(file)
def get_all_products()->List[Dict]:
    return load_products()
def save_products(products:List[Dict])->None:
    with open(DATA_FILE,"w",encoding="UTF-8") as f:
        json.dump(products,f,indent=2,ensure_ascii=False)
def add_products(product:Dict)->Dict:
    products=get_all_products()
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("Already exists")
    products.append(product)
    save_products(products)
    return product

def update_product(product_id:str, updated_product:Dict)->Dict:
    if str(updated_product.get("id")) != product_id:
        raise ValueError("Product ID must match path")
    products=get_all_products()
    for idx, existing in enumerate(products):
        if str(existing.get("id")) == product_id:
            validated = Product.model_validate(updated_product).model_dump(mode="json")
            products[idx] = validated
            save_products(products)
            return validated
    raise ValueError("Product not found")

def patch_product(product_id:str, patch_data:Dict)->Dict:
    if "id" in patch_data and str(patch_data["id"]) != product_id:
        raise ValueError("Product ID cannot be changed")
    products=get_all_products()
    for idx, existing in enumerate(products):
        if str(existing.get("id")) == product_id:
            existing.update(patch_data)
            validated = Product.model_validate(existing).model_dump(mode="json")
            products[idx] = validated
            save_products(products)
            return validated
    raise ValueError("Product not found")

def delete_product(product_id:str)->None:
    products=get_all_products()
    for idx, existing in enumerate(products):
        if str(existing.get("id")) == product_id:
            products.pop(idx)
            save_products(products)
            return
    raise ValueError("Product not found")
