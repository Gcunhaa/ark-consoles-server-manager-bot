from .base import Base, db

class Gif(Base):
    __tablename__ = "gif"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    value = db.Column(db.String, nullable=False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 