from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique=True)
    password= db.Column(db.String,nullable=False)
    phone = db.Column(db.String,nullable =False)

    def to_dict(self):
        return{
           ' id':self.id,
           'name':self.name,
           'password':self.password,
           'phone':self.phone
        }