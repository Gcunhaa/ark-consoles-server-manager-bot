from .base import Base, db

class Ticketpanel(Base):
    __tablename__ = "ticketpanel"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(2048), unique=False, nullable=False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 