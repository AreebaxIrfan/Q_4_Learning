from pydantic import BaseModel, ValidationError

# Product model
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # Optional, byDefault True
    tags: list[str] = []   # Optional, byDefault empty list

# valid data
product_data = {
    "name": "Chair",
    "price": 49.99,
    "tags": ["furniture", "wooden"]
}

product = Product(**product_data)
print(product)
print(product.model_dump())

# Invalid data
try:
    bad_product = Product(name="Table", price="free", in_stock="yes")
except ValidationError as e:
    print("\nValidation error:")
    print(e)