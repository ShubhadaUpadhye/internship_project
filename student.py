from flask import Flask,request,render_template,redirect
import mysql.connector as con

def mysql_con():
    mydb = con.connect(host='localhost', user='root', password='mysqlp@$$')
    mycursor = mydb.cursor()
    mycursor.execute("create database if not exists dept1")
    print(mydb.is_connected())
    mycursor.execute("use dept1")
    mycursor.execute("create table if not exists student_records(roll no int,names varchar(25),mail_id varchar(30),mob_no int,sem int)")
    mycursor.execute("create table if not exists attendance_sem(date int roll_no int,names varchar(50),sub1,sub2,sub3,sub4,sub5,sub6)")
    mycursor.execute("create table if not exists marks(roll_no int,names,ia1 int,ia2 int,ia3 int)")
    mycursor.execute("create database if not exists administration")
    mycursor.execute("use administartion")
    mycursor.execute("create table if not exists fees_payment(roll_no int,name varchar(25),dept varchar(),semester int,date int)")
    mycursor.execute("create table if not exists salary_payment(sl_no int,Employee_name varchar(50),Employee_domain varchar(50),dept varchar(10))")
    mycursor.execute("create table if not exists lecturers(id int name varchar(25) dept varchar(25),subjects_handled varchar(30))")

mysql_con()

def student_details():
    pass
