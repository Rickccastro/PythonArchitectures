from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    category: str
    stock: int
