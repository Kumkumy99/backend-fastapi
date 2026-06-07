from pydantic import BaseModel,Field,AnyUrl,field_validator,model_validator,computed_field,EmailStr
from typing import Annotated,Literal,Optional,List
from uuid import UUID
from datetime import datetime

class Seller(BaseModel):
    id:UUID
    name:Annotated[str,Field(
        min_length=3,
        max_length=80,
        title="Seller Name",
        description="name",
        examples=["Xiaomi Store"]
    )]
    email:EmailStr
    website:AnyUrl
    @field_validator("email",mode="after")
    @classmethod
    def validate_email(cls,value:EmailStr):
        allowed_domains=["mistore.in","hpworld.in"]
        domain=value.split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError("Invalid domain")
        return value

class Product(BaseModel):
    id:UUID
    sku:Annotated[str,
                  Field(
                      min_length=6,
                      max_length=30,
                      title="sku",
                      description="Stock keeping unit",
                      examples=["dfdfvfv","sdgyhj"]
                  )]
    name:Annotated[str,Field(
        min_length=3,
        max_length=80,
        title="Producr Name",
        description="Readeble product name",
        examples=["Xiaomi Mdel Pro"]
    )]
    description:Annotated[str,Field(
        max_length=200,
        description="Short description"
    )]
    category:Annotated[str,Field(
        min_length=3,
        max_length=30,
        description="Catgeory like mobile/laptop",
        examples=["Mobiles","Laptops"]
    )]
    brand:Annotated[str,Field(
        max_length=30,
        min_length=2,
        description="Name of the brand"
    )]
    price:Annotated[float,Field(
        gt=0,strict=True,description="Base price INR"
    )]
    currency:Literal["INR"]="INR"
    discount_percent:Annotated[int,Field(
        ge=0,le=10,description="Discount in percent(0-90)"
    )]
    tags:Annotated[Optional[List[str]],
                   Field(default=None,max_length=10,description="Upto 10 tags only")]
    img_urls:Annotated[
        List[AnyUrl],
        Field(description="Atlest one img url",max_length=1)
    ]
    stock:int
    is_active:bool
    created_at:datetime
    seller:Seller

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku(cls,value:str):
        if "-" not in value:
            raise ValueError("SKU should contain -")
        last=value.split("-")[-1]
        if len(last)!=3:
            raise ValueError("SKU must end with 3 digits")
        return value
    
    @model_validator(mode="after")
    @classmethod
    def check_multi_validity(cls,model:"Product"):
        if model.stock==0 and model.is_active is True:
            raise ValueError("Cannot activate when stock is zero")
        return model
        
    @computed_field
    @property
    def final_price(self):
        return round(self.price*self.discount_percent,2)

    