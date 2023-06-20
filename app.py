from flask import Flask, render_template,json,request,redirect,url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import webbrowser
import datetime

#==========================STARTING===================================

#app.config['UPLOAD_FOLDER'] = data/fileupload

#==========================DATE TIME===================================

now = datetime.datetime.now()

#==========================FLASK STARTER===================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pingtowinggz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#==========================DATABASE===================================

class customer_detail(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        name=db.Column(db.String(30),nullable=False)
        mobile=db.Column(db.String(20),nullable=False)
        points=db.Column(db.String(15),nullable=False)
        created_on=db.Column(db.String(2000),nullable=False)
        dob=db.Column(db.String(10),nullable=False)
    
        def to_dict(self):
                return {
                'id': self.id,
                'name': self.name,
                'mobile': self.mobile,
                'points': self.points,
                'created_on': self.created_on,
                'dob': self.dob
                }
        def __repr__(self) -> str:
                return f'{self.id}'
class customer_point_transaction(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        point_add=db.Column(db.String(10),nullable=False)
        current_points=db.Column(db.String(11),nullable=False)
        customer_details_id=db.Column(db.String(15),nullable=False)
        created_on=db.Column(db.String(20),nullable=False)
        point_type=db.Column(db.String(20),nullable=False)
        bill_amount=db.Column(db.String(20),nullable=False)
        invoice_no=db.Column(db.String(20),nullable=False)
        remark=db.Column(db.String(20),nullable=False)
    
        def to_dict(self):
                return {
                'id': self.id,
                'point_add': self.point_add,
                'current_points': self.current_points,
                'customer_details_id': self.customer_details_id,
                'created_on': self.created_on,
                'point_type': self.point_type,
                'bill_amount': self.bill_amount,
                'invoice_no': self.invoice_no,
                'remark': self.remark
                }
        def __repr__(self) -> str:
                return f'{self.id}'


#==========================DATABASE VALIDATION===================================        

import os.path
file_exists = os.path.exists('invoices.db')
if file_exists==1:
        pass
else:
        db.create_all()

#==========================CREATE DATABSE CONNECTION===================================

def create_connection():
        conn = None
        try:
                conn = sqlite3.connect("invoices.db")
                return conn
        except:
                print("error")

        return conn



@app.route('/', methods = ['GET', 'POST'])
def index():
        invoice = customer_detail.query.all()
        return render_template('TRANSACTION.html', title='Dashboard',DATA = invoice,customer_detail=customer_detail)
@app.route('/DATA', methods = ['GET', 'POST'])
def GETDATA():
        invoice = customer_point_transaction.query.all()
        return render_template('home.html', title='Dashboard',DATA = invoice,customer_point_transaction=customer_point_transaction)


@app.route('/redeem', methods = ['GET', 'POST'])
def redeemp():
        invoice = customer_point_transaction.query.all()
        return render_template('redeem.html')

@app.route('/add', methods = ['GET', 'POST'])
def addp():
        invoice = customer_point_transaction.query.all()
        return render_template('add.html')

@app.route("/set_conversion", methods=["POST"])
def upi():
        Mobile = request.form.get("mobile")
        print(Mobile)
        UPI_ID = request.form.get("pa")
        print(UPI_ID)
        
        return "saved successfully"

@app.route("/reddempoint", methods=["POST"])
def redee():
        Mobile = request.form.get("mobile")
        print(Mobile)
        point = request.form.get("pa")
        print(point)
        SECRET_ID = request.form.get("tr")
        print(SECRET_ID)
        
        conn = sqlite3.connect('pingtowinggz.db')
        c = conn.cursor()
        c.execute('SELECT money from point_conversion')
        money=c.fetchall()
        c.execute('SELECT points from point_conversion')
        p=c.fetchall()
        c.execute('SELECT points from customer_detail WHERE mobile="'+Mobile+'"')
        pointofcus=c.fetchall()
        
        pointofcustomer=(''.join(str(a)for a in pointofcus))
        print(pointofcustomer[1:-2])
        
        pointconversion=(''.join(str(a)for a in p))
        print(pointconversion[1:-2])
        
        amountofpoint=(''.join(str(a)for a in money))
        print(amountofpoint[1:-2])
        
        
        
       
        
        points=int(point)
        
        current_point=int(pointofcustomer[1:-2])-points
        
        print(current_point)
        
        from datetime import datetime

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        print(dt_string)
        
        
        pointtype="1"
        remar="done"
        
        voucher="0"
        Amount=points*(amountofpoint[1:-2])
        
        c.execute("INSERT INTO customer_point_transaction (point_add,current_points,customer_details_id,created_on,point_type,bill_amount,invoice_no,remark) VALUES ( '"+str(-points)+"', '"+str(current_point)+"','"+Mobile+"','"+dt_string+"','"+pointtype+"','"+str(Amount)+"','"+voucher+"','"+remar+"')")
        conn.commit()
        c.execute('UPDATE customer_detail set points="'+str(current_point)+'" WHERE mobile="'+Mobile+'"')
        conn.commit()
        
        
        
        return redirect(url_for("index"))

@app.route("/addpoint", methods=["POST"])
def addpointe():
        Mobile = request.form.get("mobile")
        print(Mobile)
        name = request.form.get("pa")
        print(name)
        Amount = request.form.get("pn")
        print(Amount)
        voucher = request.form.get("am")
        print(voucher)
        
        conn = sqlite3.connect('pingtowinggz.db')
        c = conn.cursor()
        c.execute('SELECT money from point_conversion')
        money=c.fetchall()
        c.execute('SELECT points from point_conversion')
        p=c.fetchall()
        c.execute('SELECT points from customer_detail WHERE mobile="'+Mobile+'"')
        pointofcus=c.fetchall()
        
        pointofcustomer=(''.join(str(a)for a in pointofcus))
        print(pointofcustomer[1:-2])
        
        pointconversion=(''.join(str(a)for a in p))
        print(pointconversion[1:-2])
        
        amountofpoint=(''.join(str(a)for a in money))
        print(amountofpoint[1:-2])
        
        
        
        points=(int(Amount)//int(amountofpoint[1:-2]))*int(pointconversion[1:-2])
        
        print(points)
        
        current_point=int(pointofcustomer[1:-2])+points
        
        print(current_point)
        
        from datetime import datetime

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        print(dt_string)
        
        
        pointtype="1"
        remar="done"
        
        
        
        c.execute("INSERT INTO customer_point_transaction (point_add,current_points,customer_details_id,created_on,point_type,bill_amount,invoice_no,remark) VALUES ( '"+str(points)+"', '"+str(current_point)+"','"+Mobile+"','"+dt_string+"','"+pointtype+"','"+Amount+"','"+voucher+"','"+remar+"')")
        conn.commit()
        c.execute('UPDATE customer_detail set points="'+str(current_point)+'" WHERE mobile="'+Mobile+'"')
        conn.commit()
        return redirect(url_for("index"))



@app.route('/api/data1')
def data1():
        return {'data': [customer_detail.to_dict() for customer_detail in customer_detail.query]}
@app.route('/api/data2')   
def data2():
        return {'data': [customer_point_transaction.to_dict() for customer_point_transaction in customer_point_transaction.query]}   
    
if __name__ == '__main__':
        app.debug = True
        url="http://127.0.0.1:"+str(8087)+"/"
        webbrowser.open_new(url)
        app.run(host="0.0.0.0",port=8087)
    