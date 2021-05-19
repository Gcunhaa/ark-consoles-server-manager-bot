from .base import Base, db

class Subscription(Base):
    __tablename__ = "subscription"

    status = db.Column(db.String(50), unique=False, nullable=False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 