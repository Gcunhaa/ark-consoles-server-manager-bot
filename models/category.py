from .base import Base, db

class Category(Base):
    __tablename__ = "category"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)