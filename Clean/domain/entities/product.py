# Entidade pura — sem dependência de frameworks ou libs externas.
# Representa um produto no sistema de compra e venda.
from dataclasses import dataclass


@dataclass
class Product:
    id: str           # UUID gerado na criação
    name: str
    description: str
    price: float
    category: str
    stock: int        # Quantidade disponível em estoque
