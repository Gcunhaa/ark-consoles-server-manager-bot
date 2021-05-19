from .base import Base, db


class LicenceSetting(Base):
    __tablename__ = "licence_setting"

    value = db.Column(db.String(100), unique=False, nullable=False)
    setting_id = db.Column(db.BigInteger,db.ForeignKey('setting.id')) 
    licence_id = db.Column(db.BigInteger,db.ForeignKey('licence.id')) 