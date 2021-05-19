from .base import Base, db


class LicenceRole(Base):
    __tablename__ = "licence_role"

    role_discord_id = db.Column(db.BigInteger, unique=False, nullable=False)
    role_id = db.Column(db.BigInteger,db.ForeignKey('role.id')) 
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 