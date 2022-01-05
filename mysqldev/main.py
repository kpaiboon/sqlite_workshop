from sqlalchemy import create_engine,DateTime,func,TIMESTAMP, Column,BigInteger, Integer, Float, String, or_, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///cmstock.db')
#@ MariaDB: Create DB "cmdev" charset=utf8mb4_general_ci (faster sorting), for use sqlalchemy charset = utf8mb4 
engine = create_engine('mysql+pymysql://root:1234@127.0.0.1/cmdev?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Product(Base):
    __tablename__ ='product'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    #time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    time_updated = Column(DateTime(timezone=True), nullable=False,server_default=func.now(),onupdate=func.now())
    #ts= Column('time_updated', TIMESTAMP, nullable=False,server_default=func.now(),onupdate=func.now())
    
Base.metadata.create_all(engine) # create table and file*.db

# Prepare data; Insert(add), commit(go)
productone = Product(name='Arduino', price=100.50, stock=10)
session.add(productone) # add single
session.commit()

# Batch Prepare data; Insert(add), commit(go)
productone = Product(name='Arduino', price=100.50, stock=10)
producttwo = Product(name='NodeMCU', price=200, stock=11)
productthree = Product(name='LED', price=1, stock=211)

#session.add(productone) # add single
session.add_all([productone,producttwo,productthree]) # add batch
session.commit()

# Query all
print('Query all')
products = session.query(Product)
for product in products:
    print(product.id,product.name,product.price,product.stock)
    

# Query with condition
print('Query with condition')
product = session.query(Product).filter(Product.name=='Arduino').first()
print(product.id,product.name,product.price,product.stock)
    

# Query with or_ condition
print('Query with or_ condition')
products = session.query(Product).filter(or_(Product.name=='Arduino',Product.name=='LED'))
for product in products:
    print(product.id,product.name,product.price,product.stock)
    
# update single
product = session.query(Product).filter(Product.id==1).first()
product.name= 'CodeOne'
product.stock= 20
session.commit()

# Query with condition
print('Query with condition')
product = session.query(Product).filter(Product.id==1).first()
print(product.id,product.name,product.price,product.stock)
    
# update multiple row
products = session.query(Product).filter(Product.name=='LED')
products.update({Product.name:'LCD'}) # key-value
session.commit()

# Query all
print('Query all')
products = session.query(Product)
for product in products:
    print(product.id,product.name,product.price,product.stock)
   
# delete name == LCD
products = session.query(Product).filter(Product.name=='LCD')
products.delete()
session.commit()

# Query all
print('Query all')
products = session.query(Product)
for product in products:
    print(product.id,product.name,product.price,product.stock)
   
   
