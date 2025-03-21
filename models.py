from db import db

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pass_phrase = db.Column(db.String(200))