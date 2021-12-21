from app import db
from app import login
from flask_login import UserMixin

class user(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True )
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(24))
    password = db.Column(db.String(128))
    Name = db.Column(db.String(128))
    def __repr__(self):
        return '<User> {}'.format(self.username,self.email,self.password,self.role)
    def serialize(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'password': self.password,
    
 }
class lop_hoc(db.Model):
    IDLopHoc = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    TenLopHoc = db.Column(db.String(140))
    GiangVien = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<Post> {}'.format(self.body)
    def serialize(self):
        return {'IDLopHoc': self.IDLopHoc,
                'TenLopHoc': self.TenLopHoc,
                'GiangVien': self.GiangVien,
             
       }

class chitiet(db.Model):
    IDChiTiet = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    IDLopHoc = db.Column(db.Integer, db.ForeignKey("lop_hoc.IDLopHoc"))
    IDUser = db.Column(db.Integer, db.ForeignKey("user.id"))

    TenDeTai = db.Column(db.String(140))
    NoiDung = db.Column(db.String(500))
    File = db.Column(db.String(140))
    NhanXet = db.Column(db.String(140))
    Diem = db.Column(db.Integer)
    DaNop = db.Column(db.Integer)
    def __repr__(self):
        return '<Post> {}'.format(self.body)
    def serialize(self):
        return {'IDChiTiet': self.IDChiTiet,
                'IDLopHoc': self.IDLopHoc,
                'IDUser': self.IDUser,
                'IDLopHoc': self.IDLopHoc,
                'TenDeTai': self.TenDeTai,
                'NoiDung': self.NoiDung,
                'File': self.File,
                'DaNop': self.DaNop,
             
       }        


@login.user_loader
def load_user(id):
    return user.query.get(int(id))