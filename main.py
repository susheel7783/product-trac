from fastapi import FastAPI,Depends
from models import Product
# from database import session  (for using db postgresql ,otherwise not needed this so in all the method we
# will use the same database for the data)
from database import session,engine
from sqlalchemy.orm import Session
import database_model  #for creating connections

# join frontend to backend 
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

# ---inetgrating fronted with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
# -----------frontend integration

database_model.Base.metadata.create_all(bind=engine)  #here we are stablishing connection to database

# get
@app.get("/")
def greet():
    return "Welcome to Telusco Trac"


products=[
    # Product(1,"Phone","budget phone",99,10),  #when we don't use BaseModel we are writing like this
    # Product(2,"Laptop","Good Laptop",999,2)
    Product(id=1,name="Phone",description="budget phone",price=99,quantity=10), #when we use BaseModel then we write like this
    Product(id=2,name="Laptop",description="Good Laptop",price=999,quantity=2),
    Product(id=3,name="Photo",description="HD photo",price=99,quantity=101),
    Product(id=4,name="Macbook",description="Mac Laptop",price=1999,quantity=2)
    ]
# in above we are passing the object manually(locally) and below we are passing the object in database
def init_db():
    db=session()
    count=db.query(database_model.Product).count()
    if count==0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        
        db.commit()
        
init_db()

# actually for each task we have to call this session so for this we will create a function get_db()
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

# fetching all the products
# @app.get("/products")
# def get_all_products():
#     # return "All Produts"
#     return products

# when we are using database use below code to get all products
@app.get("/products")
def get_all_products(db: Session=Depends(get_db)):
    # return "All Produts"
    # db=session()  instaed of calling this on each task we will call get_db() fn
    # db.query()
    db_products=db.query(database_model.Product).all()
    return db_products

# let's fetch a product by its id
# @app.get("/product/{id}")     #for getting any product localhost/product/id
# def get_product_by_id(id: int):
#     for product in products:
#         if product.id==id:
#             return product
#     return "Product not found"

# above one is for manual and below is used for database sqlalchemy
@app.get("/products/{id}")     #for getting any product localhost/product/id
def get_product_by_id(id: int,db: Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        return db_product    
    return "Product not found"

# lets add the new product so we use Post method (you can add this product from frontend or swagger)
# @app.post("/product")
# def add_product(product: Product):
#     products.append(product)
#     return product

# use below to cretae product in database
@app.post("/products")
def add_product(product: Product,db: Session=Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

# @app.put("/product")
# def update_product(id: int,product: Product):
#     for i in range(len(products)):
#         if products[i].id==id:
#             products[i]=product
#             return "Product Updated successfully"
#     return "Product not Found"    

# use below code to update in database 
@app.put("/products/{id}")
def update_product(id: int,product: Product,db: Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated"
    else:
        return "Product not Found"

     
# @app.delete("/product")
# def delete_product(id :int):
#     for i in range(len(products)):
#         if products[i].id==id:
#             del products[i]
#             return "Product Deleted"
    
#     return "Product not found"

# use below code to delete data from database
@app.delete("/products/{id}")
def delete_product(id :int,db: Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "Product not found"
    
    
# to run this activate myenv and then run the server(uvicorn main:app --reload)

# the code is running on server if we use localhost/products wea will get in json format but if we want to get good ui 
# we have to use localhost/docs 
# how to swagger click on try it out and execute if asking for parameter pass the parameter and then execute
# use postgres to use database like sqlalchemy and install postgresql driver (pip install sqlalchemy psycopg2)



#steps 
# 1. cretae a virtual env-             python -m venv myenv
# 2. activate this environement-       myenv\Scripts\Activate.ps1
# 3. install the required packages-    pip install fastapi uvicorn
# 4 for sqlite database-               pip install sqlalchemy psycopg2
# psycopg2 this is for postgresql
# run server-                          uvicorn main:app --reload