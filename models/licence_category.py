from .base import Base, db


class LicenceCategory(Base):
    __tablename__ = "licence_category"

    category_discord_id = db.Column(db.BigInteger, unique=False, nullable=False)
    category_id = db.Column(db.BigInteger,db.ForeignKey('category.id')) 
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 