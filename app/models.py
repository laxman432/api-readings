from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    clients = db.relationship('Client', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'Company name {0}, has {1} clients:\n {2}'.format(self.company_name, len(self.clients.all()),
                                                                 self.clients.all())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(140))
    client_company = db.Column(db.String(140))
    client_email = db.Column(db.String(140))
    invoice_amount = db.Column(db.Integer)
    service_description = db.Column(db.String)
    invoice_status = db.Column(db.String, unique=False, default="None")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Client name {} ({}), is to be issued {} for {}\n ' \
               'Bill will be sent to: {} '.format(self.client_company, self.client_name,
                                                  self.invoice_amount, self.service_description, self.client_email)
