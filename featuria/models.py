from datetime import datetime
from featuria import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(
        db.String(60), nullable=False, default="default.jpg")
    clients_added = db.relationship('Client', backref="creator", lazy=True)
    features_added = db.relationship('Feature', backref="creator", lazy=True)
    product_area_added = db.relationship('ProductArea', backref="creator", lazy=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return self.fullname


class Client(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    features = db.relationship('Feature', backref="client", lazy=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return self.name


class Feature(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(700), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    product_area = db.Column(db.String(60), nullable=False)
    target_date = db.Column(db.String(60), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False, default="Pending")
    date_added = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):

        return self.title


class ProductArea(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return self.title


class PriorityRange(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    range = db.Column(db.Integer, nullable=False)

    def __repr__(self):

        return self.range


