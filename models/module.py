from .base import Base, db


class Module(Base):
    __tablename__ = "module"

    name = db.Column(db.String(50), unique=False, nullable=False)