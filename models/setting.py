from .base import Base, db

class Setting(Base):
    __tablename__ = "setting"

    module_id = db.Column(db.BigInteger,db.ForeignKey('module.id')) 
    name = db.Column(db.String(50), unique=False, nullable=False)