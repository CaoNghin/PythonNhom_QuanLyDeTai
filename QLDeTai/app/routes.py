from flask import render_template
from flask.helpers import flash
from flask import redirect
from flask.wrappers import Request
from sqlalchemy.orm.session import close_all_sessions
from app import app,db
from app.forms import LoginForm, RegisterForm , ThemMoiForm 
from app.models import chitiet, lop_hoc, user
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
import sqlite3 as lite
import sys
import os
path = os.path.dirname(__file__) + "\\app.db"
con = lite.connect(path)

#############################################################################################

@app.route('/')
@app.route('/home')
@login_required
def home():
    return redirect('/dslop')

#############################################################################################
## Trang chủ sau khi Admin(Gíaoviên) đăng nhập vào ( xem tất cả lớp mà giảng viên tham gia)

@app.route('/quanli')
@login_required
def quanli():
    return render_template('Admin_quanli.html', title='Quanlipage',results=lop_hoc.query.filter_by(GiangVien=current_user.id).all(),giangvien=current_user.Name)

#############################################################################################  
## Xem danh sách sinh viên trong lớp
@app.route('/quanli/Class/<ID>')
@login_required
def Class(ID):
    dict_ht={}
    danhsachsv = user.query.all()
    for i in danhsachsv:
        dict_ht[i.id]=i.Name

    return render_template('Admin_chitietlophoc.html', title='Chitietlophoc',results=lop_hoc.query.filter_by(GiangVien=current_user.id).all(),danhsach = chitiet.query.filter_by(IDLopHoc=ID).all(),ht = dict_ht)

#############################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    
    form = LoginForm()
 
    if form.validate_on_submit():
        
        user1 = user.query.filter_by(username=form.username.data).first()
        
        if user1:
            
            pass_ok = (user1.password==form.password.data)
        if user1 is None or not pass_ok:
            flash('*Sai tên đăng nhập hoặc mật khẩu.')
            return redirect('/login')

        role = user1.role    
        login_user(user1)

        if(role=="admin"):
            next_page = '/quanli'
        else:
            next_page = '/home'    
    
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

#############################################################################################

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

#############################################################################################

@app.route('/register', methods = ['GET','POST']) 
def register():
    form = RegisterForm()

    # Nguoi dung nhap du lieu day du
    if form.validate_on_submit():
        #kiem tra username o form voi username trong db
        r_user=user.query.filter_by(username=form.r_username.data).first()
   
        # neu ton tai thi thong bao 
        if  (r_user is not None):
            flash('Username already exists')
            return redirect('/register')

        # Kiem tra form.passwordrepeat.data co trung voi form.password.data hay ko    
        if  (form.r_password.data!=form.r_passwordrepeat.data) :
            flash('password and passwordrepeat are not the same')
            return redirect('/register') 
 
        # tao moi user 
        new_user = user(
            username = form.r_username.data, 
            email = form.r_email.data, 
            role="user",
            password =  form.r_password.data)

        # dua vao csdl
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        #thong bao thanh cong o trang /index
        flash('Register successful! {}'.format(form.r_username.data))
        return redirect('/index')

    #nguoi dung khong nhap day du du lieu
    return render_template('User_register.html',title='Register' ,form=form)    

#############################################################################################
## Tạo mới lớp học và chọn danh sách sinh viên vào lớp học
@app.route('/themlop', methods=['GET', 'POST'])
@login_required
def themlop():
    form = ThemMoiForm()

    ds=user.query.filter_by(role='user').all()
    # Nguoi dung nhap du lieu day du
    if form.validate_on_submit():

        # tao moi lop_hoc
        new_class = lop_hoc(
           
            TenLopHoc = form.TenLop.data, 
            GiangVien = current_user.id)

        # dua vao csdl
        db.session.add(new_class)
        db.session.commit()

        for i in ds:
           
            if (request.form.get(str(i.id))  =="on" ):
            
                new_chitiet = chitiet(
                            IDLopHoc= lop_hoc.query.order_by(lop_hoc.IDLopHoc.desc()).first().IDLopHoc,
                            IDUser = str(i.id),
                            DaNop=0,)

                # dua vao csdl
                db.session.add(new_chitiet)
                db.session.commit()

        flash("Đã tạo lớp")  
        return redirect('/quanli')
    
    return render_template('Admin_themlop.html',title='Tạo mới lớp học' ,form=form, users = ds )              

#############################################################################################
## xem chi tiết bài nộp
@app.route('/quanli/Class/<IDLH>/<IDCT>')
@login_required
def ClassChitiet(IDLH,IDCT):
    dict_ht={}
    danhsachsv = user.query.all()
    for i in danhsachsv:
        dict_ht[i.id]=i.Name
  
    # IDChiTiet= request.args.get('IDChiTiet')

    Bainop = chitiet.query.filter_by(IDChiTiet=IDCT).all()
        
    lop = lop_hoc.query.filter_by(IDLopHoc=IDLH).first()
    return render_template('Admin_chitietbainop.html',Bainop= Bainop, lop=lop, title='Chitietbainop',results=lop_hoc.query.filter_by(GiangVien=current_user.id).all(),danhsach = chitiet.query.filter_by(IDLopHoc=IDLH).all(),ht = dict_ht)

#############################################################################################
## xem chi tiết bài nộp -> cho điểm và nhận xét
@app.route('/quanli/Class/<IDLH>/<IDCT>', methods=['POST'])
@login_required
def Chamdiem(IDLH,IDCT):
 
    NhanXet= request.form.get("NhanXet")
    Diem= request.form.get("Diem")
   
    print (":"+IDLH+"/"+IDCT)
    if NhanXet != None and NhanXet != ""  and Diem != None and Diem != "":
        
        chitiet.query.filter_by(IDChiTiet=IDCT).update(dict(NhanXet = NhanXet,Diem= Diem))
       
        db.session.commit()
      
        flash('Đã chấm điểm')  
    else:
        flash('Chấm điểm thất bại')
    return redirect('/quanli/Class/'+IDLH)



#############################################################################################
## Xoá lớp học đã chọn và toàn bộ sinh viên
@app.route('/xoalophoc')
@login_required
def xoalophoc():
    IDLop= request.args.get('IDLopHoc')

    CT = chitiet.query.filter_by(IDLopHoc=IDLop).all()
    dem=0
    
    for c in CT:
        chitiet.query.filter_by(IDChiTiet=c.IDChiTiet).delete()
        db.session.commit()
        dem=dem+1
    lop_hoc.query.filter_by(IDLopHoc=IDLop).delete()
    db.session.commit()
    flash('xoá thành công lớp và '+str(dem)+" học sinh trong lớp")
    return redirect('/quanli')

#############################################################################################
##xoá sinh viên đã chọn
@app.route('/xoasinhvientronglop')
@login_required
def xoasinhvientronglop():
    ID= request.args.get('IDChiTiet')
    c=chitiet.query.filter_by(IDChiTiet=ID).first()
    IDLH= str(c.IDLopHoc)
    
    chitiet.query.filter_by(IDChiTiet=ID).delete()
    
    
    db.session.commit()
 

    flash('xoá thành công sinh viên')
    return redirect('/quanli/Class/'+IDLH)

#############################################################################################
#  khi vào trang lớp, hiển thị danh sách các lớp của sinh viên và tình trạng đã nộp hay chưa
@app.route('/dslop')
def dslop():
    ds = chitiet.query.filter_by(IDUser=current_user.id).all()
    dict_ht={}
    danhsachlop = lop_hoc.query.all()
    for i in danhsachlop:
        dict_ht[i.IDLopHoc]=i.TenLopHoc

    return render_template('User_dslop.html',dslop= ds, dsten= dict_ht)


#############################################################################################
# chức năng nộp bài 
@app.route('/nopbai')
def nopbai():
    IDLophoc= request.args.get('malop')
    ds = lop_hoc.query.filter_by(IDLopHoc=IDLophoc).all()
    return render_template('User_nopbai.html',lop=ds)

#  chức năng nộp bài->(điền thông tin tiêu đề, nội dung, và file đính kèm)
@app.route('/nopbai', methods=['POST'])
def nopbai_upload():
    IDUser= current_user.id
    IDLophoc= request.form.get("malop")
    tendetai= request.form.get("tendetai")
    noidung= request.form.get("noidung")
    filename= ""
    uploaded_file = request.files['file']
   
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
        filename = uploaded_file.filename
        chitiet.query.filter_by(IDUser=IDUser,IDLopHoc=IDLophoc).update(dict(TenDeTai = tendetai,File= filename,NoiDung = noidung,DaNop=1))
        db.session.commit()
        flash('nop bai thanh cong')  
    else:
        flash('nop bai that bai')
    return redirect('/dslop')

#############################################################################################
#  xem chi tiết lớp học đã nộp bài
@app.route('/xemchitiet')
def xemchitiet():
    IDLophoc= request.args.get('malop')
    dsnopbai = chitiet.query.filter_by(IDUser=current_user.id,IDLopHoc=IDLophoc,DaNop =1).all()
    lop = lop_hoc.query.filter_by(IDLopHoc=IDLophoc).first()
   
    return render_template('User_chitietbainop.html',results= dsnopbai, lop=lop)
#############################################################################################
#  hủy nộp bài
@app.route('/huynopbai')
def huynopbai():
    IDUser= current_user.id
    IDLophoc= request.args.get('malop')
    chitiet.query.filter_by(IDUser=IDUser,IDLopHoc=IDLophoc).update(dict(TenDeTai = None,File= None,NoiDung = None ,DaNop=0))
    db.session.commit()
    flash('đã hủy nộp bài')  
  
    return redirect('/xemchitiet')
#############################################################################################
## tham giá lớp học bằng cách nhập mã lớp
@app.route('/thamgialophoc')
def thamgia():
    return render_template('User_thamgialophoc.html')

@app.route('/thamgialophoc', methods=['POST'])
def thamgia_lh():
    IDLophoc= request.form.get("malop")
    lophoc = chitiet.query.filter_by(IDLopHoc=IDLophoc,IDUser = current_user.id).first()
    if lophoc != None:
         flash('ban da tham gia lop hoc nay')  
         return redirect('/home')
    else:
        ds = lop_hoc.query.filter_by(IDLopHoc=IDLophoc).first()
        if ds != None:
            new_chitiet = chitiet(IDLopHoc=IDLophoc,IDUser = current_user.id,DaNop=0)
            db.session.add(new_chitiet)
            db.session.commit()
            flash('tham gia lop thanh cong')  
        else:
            flash('tham gia lop that bai') 
    return redirect('/home')
