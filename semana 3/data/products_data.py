from typing import List, Optional
from models.product_models import Product

# Base de datos simulada en memoria
products_db: List[Product] = [
    Product(id=1, name="Laptop", description="Portátil de 14 pulgadas", price=2500.0, in_stock=True),
    Product(id=2, name="Teclado", description="Mecánico RGB", price=150.0, in_stock=True),
    Product(id=3, name="Mouse", description="Gamer inalámbrico", price=80.0, in_stock=False),
]

def get_product_by_id(product_id: int) -> Optional[Product]:
    return next((p for p in products_db if p.id == product_id), None)
