from .base import Base, db



class Licence(Base):
    __tablename__ = "licence"

    user_discord_id = db.Column(db.BigInteger , unique=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
