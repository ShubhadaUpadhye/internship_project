from flask import Flask,request,render_template,redirect,Markup
import mysql.connector as con

student=Flask(__name__)
## creating mysql connection##
mydb = con.connect(host='localhost', user='root', password='mysqlp@$$')
mycursor = mydb.cursor()
###creating databae###
#mycursor.execute("create database if not exists dept1")
#print(mydb.is_connected())
mycursor.execute("use dept1")
##creating students records table using dept1 database###
#mycursor.execute("create table if not exists student_records(sl_no int ,branch varchar(15),id varchar(4),names varchar(25),mail_id varchar(30),mob_no int,sem int)")
#mycursor.execute("create table if not exists attendance_sem(date int,roll_no int,sub1 varchar(10),sub2 varchar(10),sub3 varchar(10),sub4 varchar(10),sub5 varchar(10),sub6 varchar(10))")
#mycursor.execute("create table if not exists marks(roll_no int,names,ia1 int,ia2 int,ia3 int)")
#mycursor.execute("create database if not exists administration")
#mycursor.execute("use administartion")
#mycursor.execute("create table if not exists fees_payment(roll_no int,name varchar(25),dept varchar(),semester int,date int)")
#mycursor.execute("create table if not exists salary_payment(sl_no int,Employee_name varchar(50),Employee_domain varchar(50),dept varchar(10))")
#mycursor.execute("create table if not exists lecturers(id int name varchar(25) dept varchar(25),subjects_handled varchar(30))")

@student.route("/",methods=['POST','GET'])
def home():
   if request.method=='GET':
       mydb.connect()
       return render_template("index.html")

@student.route("/login",methods=['POST','GET'])
def login():
    try:
        if request.method=='GET':
            return render_template("index.html")
    except Exception as e:
        print(e)
    else:
        if request.method=='POST':
            employee=request.form.get("employee")
            code=request.form.get("code")
            print(employee,code)
            mycursor.execute("select distinct employees,user_code from college.user_register")
            results=mycursor.fetchall()
            for i in range(len(results)):
                if employee==results[i][0] and code==results[i][1]:
                    if employee=="lecturer":
                        return render_template("student.html")
                    elif employee=="office" or employee=="admin":
                        return render_template("fees.html")
                    elif employee=="principal":
                        return render_template("salary.html")
            else:
                return render_template("index.html",error="Login Error")

@student.route("/register",methods=["GET","POST"])
def register():
    try:
        if request.method == 'GET':
            return render_template("register.html")
    except Exception as e:
        print(e)
    else:
        if request.method=='POST':
            employee=request.form.get("employee")
            code=request.form.get("code")
            print(employee,code)
            mycursor.execute("select distinct user_code,employees from college.user_register")
            user_code=mycursor.fetchall()
            for j in range(len(user_code)):
                if code==user_code[j][0]:
                    error=Markup("code already exists,Please try again")
                    return render_template("register.html",err=error)
                elif len(code)!=4 :
                    error = Markup("length of code too long,Please try again")
                    return render_template("register.html",err_1=error)
            else:
                user_upload="insert into college.user_register(employees,user_code) values(%s,%s)"
                user_insert=employee,code
                mycursor.execute(user_upload,user_insert)
                print("user registered")
                mydb.commit()
                return redirect("/")


@student.route("/add",methods=["GET","POST"])
def adding_data():
    if request.method=='GET':
        return render_template("student.html")
    else:
        if request.method=='POST':
            sl_no=request.form.get("sl_no")
            branch = request.form.get("branch")
            roll_no=request.form.get("roll_no")
            name=request.form.get("name")
            e_mail=request.form.get("email")
            mob_no=request.form.get("mob_no")
            sem=request.form.get("sem")
            print(branch,roll_no,sem,mob_no,e_mail,name)
            if branch==''or roll_no=='' or name=='' or e_mail=='' or mob_no=='' or sem=='':
                return render_template("student.html",error="Enter input")
            else:
                try:
                    add="insert into dept1.student_records(sl_no,branch,id,names,mail_id,mob_no,sem)values(%s,%s,%s,%s,%s,%s,%s)"
                    add_insert=(sl_no,branch,roll_no,name,e_mail,mob_no,sem)
                    mycursor.execute(add,add_insert)
                    print("student_record inserted")
                except Exception as e:
                    print(e)
                else:
                    mydb.commit()
                    return render_template("student.html")

'''@student.route("/update",methods=['POST','GET'])
def update():
    try:
        if request.method=='GET':
            return render_template("student.html")
    except Exception as e:
        print(e)
    else:
        if request.method == 'POST':
            data=request.form.getlist('data[]')
            for records in data:
                for k,v in records.items():
                    print(k,v)
        uploading = ("insert into student_records(branch,roll_no,names,mail_id,mob_no,sem) values(%s,%s,%s,%s,%s,%s)")
        inseritng = (branch, roll_no, name, e_mail, mob_no, sem)
        mycursor.execute(uploading, inseritng)
        mydb.commit()
        return render_template("home.html")'''

@student.route("/clear",methods=["POST","GET"])
def clear():
    try:
        mycursor.execute("truncate table dept1.student_records")
    except Exception as e:
        print(e)
    else:
        print("table truncated")
        return render_template("student.html")

@student.route("/delete",methods=["POST","GET"])
def delete():
    try:
        if request.method=="GET":
            return render_template("student.html")
    except Exception as e:
        print(e)
    else:
        if request.method=='POST':
            roll_no=request.form.get("roll_no")
            name=request.form.get("name")
            sem=request.form.get("sem")
            try:
                mycursor.execute("select * from dept1.student_records")
                mycursor.fetchall()
                delete_query="delete from dept1.student_records s where s.id=%s and s.names=%s and s.sem=%s"
                delete_instance=(roll_no,name,sem)
                mycursor.execute(delete_query,delete_instance)
                print("roll_no deleted")
            except Exception as e:
                print(e)
            else:
                mydb.commit()
                return render_template("student.html")


@student.route("/logout",methods=["POST","GET"])
def logout():
    mydb.close()
    return redirect("/")

##############student attendance#################
@student.route("/attendance",methods=["POST","GET"])
def attendance():
    try:
        if request.method=='GET':
                mycursor.execute("select * from (select date,id,names,sub1,sub2,sub3,sub4,sub5,sub6 from student_records s left join attendance_sem a on s.id=a.roll_no) as attendance_records")
                table=mycursor.fetchall()
                data=table
                return render_template("attendance.html", data=data)
        else:
            if request.method == 'POST':
                date=request.form.get("date")
                sub1 = request.form.get("sub1")
                sub2 = request.form.get("sub2")
                sub3 = request.form.get("sub3")
                sub4 = request.form.get("sub4")
                sub5 = request.form.get("sub5")
                sub6 = request.form.get("sub1")
                print(date,sub6,sub5,sub4,sub2,sub3,sub1)
                attendance_query=("insert into attendance_sem(date,sub1,sub2,sub3,sub4,sub5,sub6) values(%s,%s,%s,%s,%s,%s,%s)")
                attendance_variables=(date,sub1,sub2,sub3,sub4,sub5,sub6)
                mycursor.execute(attendance_query,attendance_variables)
                return render_template("attendance.html")
    except Exception as e:
        print(e)









if (__name__)=="__main__":
    student.run(debug=True)