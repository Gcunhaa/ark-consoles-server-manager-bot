from .base import Base, db

class Item(Base):
    __tablename__ = "Item"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.BigInteger, nullable = False, unique= False)
    role_id = db.Column(db.BigInteger, nullable = False, unique= False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id'))