from flask import Flask,request,render_template,redirect
import mysql.connector as con

student=Flask(__name__)
## creating mysql connection##
mydb = con.connect(host='localhost', user='root', password='mysqlp@$$')
mycursor = mydb.cursor()
###creating databae###
#mycursor.execute("create database if not exists dept1")
#print(mydb.is_connected())
#mycursor.execute("use dept1")
##creating students records table using dept1 database###
#mycursor.execute("create table if not exists student_records(branch varchar(15),roll_no int,names varchar(25),mail_id varchar(30),mob_no int,sem int)")
#mycursor.execute("create table if not exists attendance_sem(date int,roll_no int,sub1 varchar(10),sub2 varchar(10),sub3 varchar(10),sub4 varchar(10),sub5 varchar(10),sub6 varchar(10))")
#mycursor.execute("create table if not exists marks(roll_no int,names,ia1 int,ia2 int,ia3 int)")
#mycursor.execute("create database if not exists administration")
#mycursor.execute("use administartion")
#mycursor.execute("create table if not exists fees_payment(roll_no int,name varchar(25),dept varchar(),semester int,date int)")
#mycursor.execute("create table if not exists salary_payment(sl_no int,Employee_name varchar(50),Employee_domain varchar(50),dept varchar(10))")
#mycursor.execute("create table if not exists lecturers(id int name varchar(25) dept varchar(25),subjects_handled varchar(30))")

@student.route("/",methods=['POST','GET'])
def home():
    try:
        if request.method=='GET':
            render_template("index.html")
    except Exception as e:
        print(e)
    else:
        return render_template("index.html")

@student.route("/login",methods=['POST','GET'])
def login():
    try:
        if request.method=='GET':
            return render_template("index.html")
        else:
            if request.method=='POST':
                employee=request.form.get("employee")
                code=request.form.get("code")
                print(employee,code)
                mycursor.execute("select * from college.user_register where employees like employee and user_code like code")
                mycursor.fetchall()
            else:
                return render_template("index.html",errorr="Login Error")
    except Exception as e:
        print(e)
    else:
        return render_template("student.html")

@student.route("/register",methods=["GET","POST"])
def register():
    try:
        if request.method == 'GET':
            return render_template("register.html")
        else:
            if request.method=='POST':
                employee=request.form.get("employee")
                code=request.form.get("code")
                print(employee,code)
                if len(code)!=4:
                    render_template("register.html",error="length of code is long,Kindly re-enter code")
    except Exception as e:
        print(e)
    else:
        user_upload="insert into user_register code values(%s)"
        user_insert=employee,code
        mycursor.execute(user_upload,user_insert)
    return redirect("/")


'''@student.route("/add",methods=["GET"])
def adding_data():
    try:
        if request.method=='POST':
            branch = request.form.get("branch")
            roll_no=request.form.get("roll_no")
            name=request.form.get("name")
            e_mail=request.form.get("email")
            mob_no=request.form.get("mob_no")
            sem=request.form.get("sem")
            if branch==''or roll_no=='' or name=='' or e_mail=='' or mob_no=='' or sem=='':
                return render_template("students.html",error="Enter input")
            add="insert into student_records branch,roll_no,names,mail_id,mob_no,sem values(%s,%s,%s,%s,%s,%s"
            add_insert=(branch,roll_no,name,e_mail,mob_no,sem)
            mycursor.execute(add,add_insert)
    except Exception as e:
        return(e)
    finally:
        if request.method=='GET':
            render_template("students.html")

@student.route("/add",methods=['POST','GET'])
def add():
    if request.method == 'POST':
        branch = request.form.get("branch")
        roll_no = request.form.get("roll_no")
        name = request.form.get("name")
        e_mail = request.form.get("email")
        mob_no = request.form.get("mob_no")
        sem = request.form.get("sem")
    uploading = ("insert into student_records(branch,roll_no,names,mail_id,mob_no,sem) values(%s,%s,%s,%s,%s,%s)")
    inseritng = (branch, roll_no, name, e_mail, mob_no, sem)
    mycursor.execute(uploading, inseritng)
    mydb.commit()
    return render_template("home.html")

@student.route("/",methods=["GET","POST"])
def update():
    update_list=[]
    orginial_list=[]
    mycursor.execute("select * from student_records")
    for all in mycursor.fetchall():
        orginial_list.append(all)
    if request.method=='GET':
        return render_template("index.html")
    if request.method == 'POST':
        branch = request.form.get("branch")
        update_list.append(branch)
        roll_no = request.form.get("roll_no")
        update_list.append(roll_no)
        name = request.form.get("name")
        update_list.append(name)
        e_mail = request.form.get("email")
        update_list.append(e_mail)
        mob_no = request.form.get("mob_no")
        update_list.append(mob_no)
        sem = request.form.get("sem")
        update_list.append(sem)
    print(update_list)
    for originals in orginial_list:
        for updates in update_list:
            if originals!=updates:
               print(updates)
        break
    return render_template("index.html")
'''




if (__name__)=="__main__":
    student.run(debug=True)