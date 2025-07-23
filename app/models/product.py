class Product:
    def __init__(self, id, name, price, stock, description=None, image=None):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
        self.image = image