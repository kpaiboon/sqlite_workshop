from sqlalchemy import create_engine,DateTime,func,TIMESTAMP, Column,BigInteger, Integer, Float, String, or_, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///cmstock.db')
engine = create_engine('postgresql://postgres:1234@localhost:5432/cmdev')
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
products = session.query(Product).filter(or_(Product.name=='Arduino',Product.name=='NodeMCU'))
for product in products:
    print(product.id,product.name,product.price,product.stock)
    

