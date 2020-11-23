from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import datetime

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

app = Flask(__name__)
app.after_request(after_request)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/input_store'
# 设置数据库
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'person'
    Id=db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Text = db.Column(db.Text)
    Year=db.Column(db.String(255), default=str(datetime.datetime.now()).split('-')[0])
    updatetime=db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return self

@app.route('/all', methods=['GET', 'POST'])
def all():
    year=str(datetime.datetime.now()).split('-')[0]
    person=Person.query.filter(Person.Year==year).order_by(-Person.updatetime).all()
    PR=[]
    for i in range(len(person)):
        pr={'name':person[i].Name,'text':person[i].Text}
        PR.append(pr)
    return jsonify(PR)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=="GET":
        name=request.args.get('name')
        text=request.args.get('text')
        id=request.args.get('id')
    else:
        name=request.json.get('name')
        text=request.json.get('text')
        id = request.json.get('id')
    id=int(id)
    if id==0:
        person=Person(Name=name,Text=text)
    else:
        person=Person.query.filter(Person.Id==id).all()[0]
        person.Text=text
        person.updatetime=datetime.datetime.now()
    db.session.add(person)
    db.session.commit()
    return jsonify([{'code':200,'id':person.Id}])

if __name__ == '__main__':
    app.run(debug=True)

