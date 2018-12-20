from handRecog.app import db

class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m1 = db.Column(db.String)
    m2 = db.Column(db.String)
    m3 = db.Column(db.String)
    m4 = db.Column(db.String)
    m5 = db.Column(db.String)
    m6 = db.Column(db.String)
    m7 = db.Column(db.String)
    result = db.Column(db.Integer)

    def __init__(self, m1, m2, m3, m4, m5, m6, m7, result):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.m5 = m5
        self.m6 = m6
        self.m7 = m7
        self.result = result