from .base import Base, db

class Economy(Base):
    __tablename__ = "Economy"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    user_discord_id = db.Column(db.BigInteger, nullable = False, unique= False)
    wallet = db.Column(db.BigInteger, nullable = False, unique= False)
    bank = db.Column(db.BigInteger, nullable = False, unique= False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id'))