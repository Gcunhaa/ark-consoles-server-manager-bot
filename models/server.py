from .base import Base, db


class Server(Base):
    __tablename__ = "server"

    server_discord_id = db.Column(db.BigInteger, unique=False, nullable=False)
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 