#let's import basemodel if we are using basemodel no need to create Constructor and in main file 
# def __init__(self,id:int, name:str,description:str, price:float, quantity: int):
#         self.id=id
#         self.name=name
#         self.description=description
#         self.price=price
#         self.quantity=quantity

from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int 


# this is for pydantic 

# use this if you don't use BaseModel

# class Product:
#     id: int
#     name: str
#     description: str
#     price: float
#     quantity: int

    # def __init__(self,id:int, name:str,description:str, price:float, quantity: int):
    #     self.id=id
    #     self.name=name
    #     self.description=description
    #     self.price=price
    #     self.quantity=quantity