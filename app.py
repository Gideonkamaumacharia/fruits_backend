from flask import Flask,request,jsonify
from flask_migrate import Migrate
from models import User
from models import db
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
from flask_cors import CORS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fruits.db'
app.config['SQLALCHEMY_TRACK_MODIICATIONS'] = False
app.config['JWT_SECRET_KEY']= '45dea5f0e12e23b2208a6c67917002fcb4a23b77b0b1ec897b1a0f131833043c'
CORS(app)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)
db.init_app(app)

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message':'Invalid Json'})
    password_hash = bcrypt.generate_password_hash(data.get('password'))
    new_user =  User(name=data.get('name'),email=data.get('email'),password=password_hash,phone=data.get('phone'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'User registered successfully'})

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email = data.get('email')).first()
    if not user:
        return jsonify({'message':'User does not exist'})
    if not bcrypt.check_password_hash(user.password,data.get('password')):
        return jsonify({'message':'Inavlid password'})
    access_token = create_access_token(identity=user.id)
    return {'access_token':access_token}

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_data = [user.to_dict() for user in users]
    return jsonify(user_data)
    
if __name__ == "__main__":
    app.run(debug=True)