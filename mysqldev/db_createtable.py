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
session.add(productone)
session.commit()
