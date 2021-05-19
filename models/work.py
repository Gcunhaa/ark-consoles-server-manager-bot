from .base import Base, db

class Work(Base):
    __tablename__ = "Work"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)
    min_value = db.Column(db.BigInteger, nullable = False, unique= False)
    max_value = db.Column(db.BigInteger, nullable = False, unique= False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id'))