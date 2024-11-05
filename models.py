from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    linkedId = db.Column(db.Integer, nullable=True)  # Link to another contact's ID
    linkPrecedence = db.Column(db.String, default="primary")  # "primary" or "secondary"
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "linkedId": self.linkedId,
            "linkPrecedence": self.linkPrecedence,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "deletedAt": self.deletedAt,
        }
