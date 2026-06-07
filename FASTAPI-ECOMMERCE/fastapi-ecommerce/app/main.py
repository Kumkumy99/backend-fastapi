from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import AnyUrl, BaseModel

from schema.product import Product, Seller
from service.products import (
    get_all_products,
    update_product,
    patch_product,
    delete_product,
)
from uuid import uuid4
from datetime import datetime

app = FastAPI()
@app.get('/')
def root():
    return {"msg":"welcome to fastapi"}

#@app.get("/products")
#def get_products():
#    return get_all_products()
@app.get("/products")
def list_products(
    name:str=Query(default=None,
                                 min_length=1,
                                 max_length=10,
                                 description="SEARCH BY NAME{CASE INSENSITIVE}"),
                  sort_by_price:bool=Query(default=False,
                                           description="Sort products by their price"),
                  order:str=Query(default="asc",
                                  description="sort order when sort_by_price=true(asc,desc)"),
                  limit:int=Query(default=10,ge=1,le=10,description="limit"),
                  offset:int=Query(default=0,description="Pagination")):
    products = get_all_products()
    fproducts = products
    if name:
        needle=name.strip().lower()
        fproducts=[p for p in products if needle in p.get("name","").lower()]
        if not fproducts:
            raise HTTPException(status_code=404,detail="No product matches")
    
    if sort_by_price:
        reverse=order=="desc"
        fproducts=sorted(fproducts,key=lambda p:p.get("price",0),reverse=reverse)
    total =len(fproducts)
    fproducts=fproducts[offset:offset+limit:1]
    return {
        "total":total,
        "items":fproducts
    }

@app.get("/products/{product_id}")
def get_product_by_id(product_id:str):
    products=get_all_products()
    for product in products:
        if product["id"]==product_id:
            return product
    raise HTTPException(status_code=404,detail="Product not found")

@app.put("/products/{product_id}")
def replace_product(product_id:str, product:Product):
    if str(product.id) != product_id:
        raise HTTPException(status_code=400, detail="Product ID in body must match path")
    try:
        return update_product(product_id, product.model_dump(mode="json"))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.patch("/products/{product_id}")
def patch_product_by_id(product_id:str, product:ProductPatch):
    patch_data = product.model_dump(exclude_unset=True, mode="json")
    if not patch_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    try:
        return patch_product(product_id, patch_data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.delete("/products/{product_id}", status_code=204)
def delete_product_by_id(product_id:str):
    try:
        delete_product(product_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return

@app.post("/products",status_code=201)
def create_products(product:Product):
    product_dict=product.model_dump(mode="json")
    product_dict["id"]=uuid4()
    product_dict["created_at"]=datetime.utcnow().isoformat()
    try:
        products.append(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    return product.model_dump(mode="json")
