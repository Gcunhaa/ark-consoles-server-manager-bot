from .base import Base, db


class LicenceChannel(Base):
    __tablename__ = "licence_channel"

    channel_discord_id = db.Column(db.BigInteger, unique=False, nullable=False)
    channel_id = db.Column(db.BigInteger,db.ForeignKey('channel.id')) 
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 