from flask import Flask,request,render_template,redirect,Markup
import mysql.connector as con

student=Flask(__name__,template_folder='templates')
## creating mysql connection##
mydb = con.connect(host='localhost', user='root', password='mysqlp@$$')
mycursor = mydb.cursor()
###creating databae###
#mycursor.execute("create database if not exists dept1")
#print(mydb.is_connected())
mycursor.execute("use dept1")
mycursor.execute("create database if not exists marks")
##creating students records table using dept1 database###
mycursor.execute("create table if not exists student_records(sl_no int ,branch varchar(15),id varchar(4),names varchar(25),mail_id varchar(30),mob_no int,sem int)")
mycursor.execute("create table if not exists dept1.attendance_sem(date int,sem int ,roll_no int,sub1 varchar(10),sub2 varchar(10),sub3 varchar(10),sub4 varchar(10),sub5 varchar(10),sub6 varchar(10))")
#mycursor.execute("create table if not exists marks(roll_no int,names,ia1 int,ia2 int,ia3 int)")
#mycursor.execute("create database if not exists administration")
#mycursor.execute("use administartion")
#mycursor.execute("create table if not exists fees_payment(roll_no int,name varchar(25),dept varchar(),semester int,date int)")
#mycursor.execute("create table if not exists salary_payment(sl_no int,Employee_name varchar(50),Employee_domain varchar(50),dept varchar(10))")
#mycursor.execute("create table if not exists lecturers(id int name varchar(25) dept varchar(25),subjects_handled varchar(30))")

############################################home#############################################
@student.route("/",methods=['POST','GET'])
def home():
   if request.method=='GET':
       mydb.connect()
       return render_template("index.html")

################################login#################################################
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
                        return render_template("salary.html")
                    elif employee=="principal":
                        return render_template("salary.html")
            else:
                return render_template("index.html",error="Login Error")

#############################################register#################################################################
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

########################student detials with lecturers################################
@student.route("/add_students",methods=["GET","POST"])
def adding_data():
    student_list=[]
    try:
        if request.method=='POST':
            sl_no=request.form.get("sl_no")
            branch = request.form.get("branch")
            roll_no=request.form.get("roll_no")
            name=request.form.get("name")
            e_mail=request.form.get("email")
            mob_no=request.form.get("mob_no")
            sem=request.form.get("sem")
            print(sl_no,branch,roll_no,sem,mob_no,e_mail,name,mob_no)
            student_list.append((sl_no,branch,roll_no,name,e_mail,mob_no,sem))
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
    except Exception as e:
        print(e)
    else:
        return render_template("student.html")

@student.route("/display_records",methods=['POST','GET'])
def display_records():
    try:
        if request.method=='GET':
            mycursor.execute("select * from dept1.student_records")
            data=mycursor.fetchall()
            return render_template("print.html",data=data)
    except Exception as e:
        print(e)


@student.route("/student_details",methods=['POST','GET'])
def display_students():
    if request.method=="GET":
        return render_template("Print.html")
    else:
        if request.method=="POST":
            semester=request.form.get("semester")
            date_from=request.form.get("date_from")
            to_date=request.form.get("to_date")
            print(semester,date_from,to_date)
            if semester=="all":
                mycursor.execute("select * from dept1.student_records s left join dept1.attendance_sem a on s.sem=a.sems")
                data=mycursor.fetchall()
                return render_template("Print.html",data=data)
            else:
                try:
                    query=("select * from dept1.student_records s left join dept1.attendance_sem a on s.sem=a.sems  where sem=%s order by id asc")
                    fetch=semester
                    mycursor.execute(query,(fetch,))
                    data=mycursor.fetchall()
                    print(data)
                    return render_template("Print.html",data=data)
                except Exception as e:
                    print(e)



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
        return render_template("salary.html")'''

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


###############################################student attendance##################################################3
@student.route("/add_attendance",methods=["POST","GET"])
def attendance_table():
    try:
        mycursor.execute("use dept1")
        mycursor.execute("create table if not exists attendance_sem(date date,sem int,roll_no int,sub1 varchar(10),sub2 varchar(10),sub3 varchar(10),sub4 varchar(10),sub5 varchar(10),sub6 varchar(10))")
    except Exception as e:
        print(e)
    else:
        print("tables created")
    def add_attendance():
        try:
            if request.method == 'POST':
                date=request.form.get("date")
                sem=request.form.get("sem")
                roll_no=request.form.get("roll_no")
                sub1 = request.form.get("sub1")
                sub2 = request.form.get("sub2")
                sub3 = request.form.get("sub3")
                sub4 = request.form.get("sub4")
                sub5 = request.form.get("sub5")
                sub6 = request.form.get("sub1")
                print(date,sub6,sub5,sub4,sub2,sub3,sub1)
                if date=="" or sub1=="" or sub2=="" or sub3=="" or sub4=="" or sub5=="" or sub6=="":
                    return render_template("attendance.html",error="enter attendance")
                else:
                    try:
                        attendance_query=("insert into attendance_sem(date,sem,roll_no,sub1,sub2,sub3,sub4,sub5,sub6) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                        attendance_variables=(date,sem,roll_no,sub1,sub2,sub3,sub4,sub5,sub6)
                        mycursor.execute(attendance_query,attendance_variables)
                    except Exception as e:
                        print(e)
                    else:
                        mydb.commit()
        except Exception as e:
            print(e)
        else:
            print("attendance data added")
    add_attendance()
    return render_template("attendance.html")

@student.route("/delete_attendance",methods=["POST","GET"])
def delete_attendance():
    try:
        mycursor.execute("use dept1")
        mycursor.execute("select * from student_records s left join attendance_sem a on s.id=a.roll_no")
        table = mycursor.fetchall()
        data = table
        if request.method == 'GET':
            return render_template("attendance.html", data=data)
        else:
             if request.method=="POST":
                date=request.form.get("date")
                roll_no=request.form.get("roll_no")
                sem=request.form.get("sem")
                if date=="" or roll_no=="" or sem=="":
                   return render_template("attendance.html",error="enter input")
                else:
                    try:
                       mycursor.execute("select date,roll_no,sem from college.salary")
                       mycursor.fetchall()
                       delete_query = "delete from dept1.attendance_sem a where a.date=%s and a.roll=%s and a.sem=%s"
                       delete_instance = (date,roll_no,sem)
                       mycursor.execute(delete_query, delete_instance)
                       print("salary of this person deleted")
                    except Exception as e:
                       print(e)
                    else:
                       mydb.commit()
                       return render_template("student.html")
    except Exception as e:
       print(e)
    else:
       print("attendace_deleted")

@student.route("/clear_attendance",methods=["POST","GET"])
def clear_attendance():
    try:
        mycursor.execute("truncate table dept1.attendance_sem")
    except Exception as e:
        print(e)
    else:
        print("table truncated")
        return render_template("attendance.html")

#######################################################student marks##########################################################################3333
@student.route("/marks",methods=["GET"])
def marks():
    if request.method=='GET':
        return  render_template("marks.html")

@student.route("/add_marks",methods=["POST","GET"])
def marks_table():
    try:
        mycursor.execute("use marks")
        mycursor.execute("create table if not exists ia1(sl_no int,roll_no int,sem int,sub1 float,sub2 float,sub3 float,sub4 float,sub5 float,sub6 float)")
        mycursor.execute("create table if not exists ia2(sl_no int,roll_no int,sem int,sub1 float,sub2 float,sub3 float,sub4 float,sub5 float,sub6 float)")
        mycursor.execute("create table if not exists ia3(sl_no int,roll_no int,sem int,sub1 float,sub2 float,sub3 float,sub4 float,sub5 float,sub6 float)")
    except Exception as e:
        print(e)
    else:
        print("database and table created")
    def add_marks():
        try:
            if request.method=='POST':
                sl_no=request.form.get("sl_no")
                roll_no=request.form.get("roll_no")
                sem=request.form.get("sem")
                sub1 = request.form.get("sub1")
                sub2 = request.form.get("sub2")
                sub3 = request.form.get("sub3")
                sub4 = request.form.get("sub4")
                sub5 = request.form.get("sub5")
                sub6 = request.form.get("sub1")
                print(roll_no,sub6, sub5, sub4, sub2, sub3, sub1)
                if  sub1 == "" or sub2 == "" or sub3 == "" or sub4 == "" or sub5 == "" or sub6 == "":
                    return render_template("marks.html",error="enter attendance")
                else:
                    mark_query=("insert into marks.ia1(sl_no,roll_no,sem,sub1,sub2,sub3,sub4,sub5,sub6) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    marks_upload=(sl_no,roll_no,sem,sub1, sub2, sub3, sub4, sub5, sub6)
                    mycursor.execute(mark_query,marks_upload)
                    mydb.commit()
        except Exception as e:
            print(e)
        else:
            print("marks_table created")
    add_marks()
    return render_template("marks.html")

#############################################salary_payment################################################
@student.route("/add_salary",methods=["POST","GET"])
def salary_table():
    mycursor.execute("use college")
    mycursor.execute("create table if not exists salary(sl_no int,date date,unique_id varchar(15),names varchar(30),employee_type varchar(30),dept varchar(50),sem_taken varchar(30),allowances double,deductions double,gross_salary double,net_salary double,status varchar(15))")
    print("table created")
    def add_salary():
        try:
            if request.method=='POST':
                sl_no=request.form.get("sl_no")
                date=request.form.get("date")
                u_id=request.form.get("u_id")
                name=request.form.get("name")
                employee=request.form.get("employee")
                dept=request.form.get("dept")
                sem=request.form.get("sem")
                allowance=request.form.get("allowance")
                deduction=request.form.get("deduction")
                gross_salary=request.form.get("gross_salary")
                net_salary=request.form.get("net_salary")
                status=request.form.get("status")
                print(name,u_id)
                if sl_no=="" or date=="" or u_id=="" or name=="" or employee=="" or dept=="" or sem=="" or allowance=="" or deduction=="" or gross_salary=="" or net_salary=="" or status=="":
                    return render_template("salary.html",error="enter input")
                else:
                    try:
                        add_salary_query="insert into college.salary(sl_no,date,unique_id,names,employee_type,dept,sem_taken,allowances,deductions,gross_salary,net_salary,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        salary_upload=(sl_no,date,u_id,name,employee,dept,sem,allowance,deduction,gross_salary,net_salary,status)
                        mycursor.execute(add_salary_query,salary_upload)
                    except Exception as e:
                        print(e)
                    else:
                        mydb.commit()
                        print('salaries added')
        except Exception as e:
            print(e)
        else:
            print("executed")
    add_salary()
    return render_template("salary.html")

@student.route("/delete_salary",methods=["POST","GET"])
def delete_salary():
   try:
       if request.method=="GET":
           return render_template("salary.html")
       else:
           if request.method=="POST":
               name=request.form.get("name")
               u_id=request.form.get("u_id")
               if name=="" or u_id=="":
                   return render_template("salary.html",error="enter input")
               else:
                   try:
                       mycursor.execute("select u_id,names from college.salary")
                       mycursor.fetchall()
                       delete_query = "delete from college.salary c where c.unique_id=%s and c.names=%s"
                       delete_instance = (u_id,name)
                       mycursor.execute(delete_query, delete_instance)
                       print("salary of this person deleted")
                   except Exception as e:
                       print(e)
                   else:
                       mydb.commit()
                       return render_template("student.html")
   except Exception as e:
       print(e)
   else:
       return render_template("salary.html")

@student.route("/clear_salary",methods=["POST","GET"])
def salary_clear():
    try:
        mycursor.execute("truncate table college.salary")
    except Exception as e:
        print(e)
    else:
        print("table truncated")
        return render_template("student.html")

############################logout###############################################
@student.route("/logout",methods=["POST","GET"])
def logout():
    mydb.close()
    return redirect("/")

if (__name__)=="__main__":
    student.run(debug=True)