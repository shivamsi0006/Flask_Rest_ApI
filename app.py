from flask import Flask ,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.sqlite3'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(250))
    email=db.Column(db.String(250),unique=True)
    password=db.Column(db.String(250))
    def __repr__(self):
        return f'{self.name}'

@app.route('/register',methods=['POST'])
def register():
    name=request.get_json().get('name')
    email=request.get_json().get('email')
    password=request.get_json().get('password')
    user=User.query.filter_by(email=email).first()
    
    if user:
        return jsonify({'message':'user already exist'})
    insert_user=User(name=name,email=email,password=password)
    db.session.add(insert_user)
    db.session.commit()
    return jsonify({'message':'user update successfuly'})

@app.route('/login',methods=["POST"])
def login():
    email=request.get_json().get('email')
    password=request.get_json().get('password')
    verify_user=User.query.filter_by(email=email).first()
    if not verify_user:
        return jsonify({"message":"user email does not exist"})
    if password!=verify_user.password:
        return jsonify({"message":"user password does not match"})
    data={"id":verify_user.id,"name":verify_user.name,"email":verify_user.email,"password":verify_user.password}
    return jsonify(data)


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
