from .base import Base, db

class Channel(Base):
    __tablename__ = "channel"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)