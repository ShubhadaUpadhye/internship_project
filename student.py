from flask import Flask,request,render_template,redirect,Markup
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
    try:
        if request.method=='GET':
            return render_template("student.html")
    except Exception as e:
        return (e)
    else:
        if request.method=='POST':
            branch = request.form.get("branch")
            roll_no=request.form.get("roll_no")
            name=request.form.get("name")
            e_mail=request.form.get("email")
            mob_no=request.form.get("mob_no")
            sem=request.form.get("sem")
            if branch==''or roll_no=='' or name=='' or e_mail=='' or mob_no=='' or sem=='':
                return render_template("student.html",error="Enter input")
            else:
                try:
                    add="insert into dept1.student_records(branch,roll_no,names,mail_id,mob_no,sem)values(%s,%s,%s,%s,%s,%s)"
                    add_insert=(branch,roll_no,name,e_mail,mob_no,sem)
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
    except Exception as e :
        print(e)
    else:
        if request.method=='POST':
            roll_no=request.form.get("roll_no")
            try:
                mycursor.execute("select distinct roll_no from dept1.student_record")
                ids=mycursor.fetchall()
                for id in range(len(ids)):
                    if roll_no==ids[id][0]:
                        mycursor.execute("delete from dept1.student_records where roll_no='{}'.format(roll_no)")
                        break
                    else:
                        return render_template("student.html",error="Roll_no doesnt not exist")
            except Exception as e:
                print(e)
            finally:
                mydb.commit()
                return render_template("student.html")
'''
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
@student.route("/logout",methods=["POST","GET"])
def logout():
    mydb.close()
    return redirect("/")


if (__name__)=="__main__":
    student.run(debug=True)