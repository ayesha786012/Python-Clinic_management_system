# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
import base64

import MySQLdb
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL

import json

app = Flask(__name__)
app.secret_key = "12345"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "logininfo"
db = MySQL(app)


####          login           ###
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form['password'].encode("ascii")
            encoded = base64.b64encode(password)
            decoded = encoded.decode('ascii', 'strict')
            # database connectivity
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            print(cursor.execute("SELECT password FROM log WHERE email LIKE %s", (username,)))
            check = cursor.fetchone()
            print(check)
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM log WHERE email=%s AND password=%s",
                           ([username], [decoded]))
            print(password)
            print(decoded)
            print(encoded)
            info = cursor.fetchone()
            print(info)
            if info is not None:
                if info["email"] == username and info["password"] == decoded:
                    session['Loginsuccessful'] = True
                    if info["password"]=='YWRtaW4=':
                     return redirect(url_for('profile'))
                return redirect(url_for('patients_profile'))

            else:
                return redirect(url_for('new_user'))
    return render_template("login.html")


####          REGISTRATION            ###
@app.route('/new', methods=['GET', 'POST'])
def new_user():
    # print('1');
    if request.method == 'POST':
        if "name" in request.form and "email" in request.form and "password" in request.form:
            username = request.form['name']

            email = request.form['email']
            password = request.form['password'].encode("ascii")
            encoded = base64.b64encode(password)
            decoded = encoded.decode('ascii', 'strict')
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO logininfo.log(name,email,password) VALUES(%s,%s,%s)",
                           (username, email, decoded))
            # print('2')
            # print('b');
            print('REgister');
            print(password)
            print(decoded)
            # print(encoded)
            # hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template("register.html")


@app.route('/new/profile')
def profile():
    if session['Loginsuccessful'] == True:
        return render_template("profile.html")

@app.route('/new/patients_profile')
def patients_profile():
    if session['Loginsuccessful'] == True:
        return render_template("patients_profile.html")


@app.route('/new/Doctor')
def Doctor():
    return render_template("Doctor.html")


@app.route('/logout')
def logout():
    if session.pop('Loginsuccessful', None):
        return redirect(url_for('index'))
@app.route('/new/book_an_appoinment_patientSite')
def book_an_appoinment_patientSite():
    return render_template("book_appoinment-patientsSite.html")


@app.route('/new/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        if "patients_first_name" in request.form and "patients_Last_name" in request.form and "patients_father_name" in request.form and "patients_Address_name" in request.form and "patients_email_Address_name" in request.form and "patients_Phone_Number" in request.form:
            patientsfname = request.form['patients_first_name']
            patientslname = request.form['patients_Last_name']
            patientsfathername = request.form['patients_father_name']
            patientsaddressname = request.form['patients_Address_name']
            patientsEMAILaddressname = request.form['patients_email_Address_name']
            patientsphone_number = request.form['patients_Phone_Number']
            # password = request.form['password'].encode("ascii")
            # encoded = base64.b64encode(password)
            # decoded = encoded.decode('ascii', 'strict')
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO logininfo.patients(patients_first_name,patients_last_name,Patients_father_name,Patient_address,Patients_email_address,patients_phone_number) VALUES(%s,%s,%s,%s,%s,%s)",
                (patientsfname, patientslname, patientsfathername, patientsaddressname, patientsEMAILaddressname,
                 patientsphone_number))
            db.connection.commit()
            cursor.close()
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            patients_RECORD = cursor.execute("SELECT * FROM patients ")
            # patients_RECORD = cursor.execute("SELECT * FROM logininfo.patients WHERE patients_first_name=%s", ([patients]))
            """Api to retive all the patient from the database"""
            if (patients_RECORD) > 0:
                user_details = cursor.fetchall()
                print(user_details)
                # db.connection.commit()
            return render_template("Patients.html", user_details=user_details)
            # return render_template("pateints_record_register.html")
            # return redirect(url_for(''))
        # return redirect(url_for('get'))

    return render_template("Patients.html")


# @app.route('/new/RECORD_patients')


@app.route('/new/action_page', methods=['GET', 'POST'])
def livesearch():
    searchbox = request.form.get("livebox")
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "select * from patients where patients_first_name LIKE '{}%' order by idPatients".format(searchbox)
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)


# def lom():
# if request.method == 'POST':
#   if "search" in request.form:
#      search = request.form["search"]
#   print(search)
#  cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
# patients_RECORDed = cursor.execute("SELECT * FROM patients WHERE patients_first_name LIKE %s",
# ([search],))
# patients_RECORD = cursor.execute(")
# """Api to restive all the patient from the database"""
#  print(patients_RECORDed)
#  if patients_RECORDed > 0:
#     user_details = cursor.fetchall()
#    print(user_details)
# db.connection.commit()
#  return render_template("Patients.html", user_details=user_details)

# return render_template("Patients.html")

# the method which is used to delete

# @app.route("/ajax_add",methods=["POST","GET"])
# def ajax_add():
# if request.method == 'POST':
# cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
# patients_first_name = request.form['patients_first_name']
# patients_last_name = request.form['patients_last_name']
###Patient_address = request.form['Patient_address']
# Patients_email_address = request.form['Patients_email_address']
# patients_phone_number = request.form['patients_phone_number']
# print(txtname)
# if patients_first_name == '':
# msg = 'Please Input name'
# elif patients_last_name == '':
# msg = 'Please Input Department'
# elif Patients_father_name == '':
# msg = 'Please Input Phone'
# elif Patient_address == '':
# msg = 'Please Input Department'
# elif Patients_email_address == '':
# msg = 'Please Input Phone'
# elif patients_phone_number == '':
# msg = 'Please Input Phone'
# else:
# cur.execute(
# "INSERT INTO logininfo.patients(patients_first_name,patients_last_name,Patients_father_name,Patient_address,Patients_email_address,patients_phone_number) VALUES(%s,%s,%s,%s,%s,%s)",
# (patients_first_name, patients_last_name, Patients_father_name, Patient_address,Patients_email_address,patients_phone_number))
# db.connection.commit()
# cur.close()
# msg = 'New record created successfully'
# return jsonify(msg)

@app.route("/ajax_delete", methods=["POST", "GET"])
def ajax_delete():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('delete  from patients where idPatients={0}'.format(getid))
        cur.execute('ALTER TABLE patients AUTO_INCREMENT = 1')
        db.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


@app.route("/ajax_update", methods=["POST", "GET"])
def ajax_update():
    if request.method == 'POST':
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        string = request.form['string']
        patients_f_name = request.form['patients_f_name']
        patients_l_name = request.form['patients_l_name']
        Patients_father_name = request.form['Patients_father_name']
        Patient_address = request.form['Patient_address']
        Patients_email_address = request.form['Patients_email_address']
        patients_phone_number = request.form['patients_phone_number']
        print(string)
        if patients_f_name == '' and patients_l_name == '' and Patients_father_name == '' and Patient_address == '' and Patients_email_address == '' and patients_phone_number == '':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif patients_f_name == '':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif patients_l_name == '':
            msg = 'Please Input Last_name'
            return jsonify(msg)
        elif Patients_father_name == '':
            msg = 'Please Input Father_name'
            return jsonify(msg)
        elif Patient_address == '':
            msg = 'Please Input Address'
            return jsonify(msg)
        elif Patients_email_address == '':
            msg = 'Please Input Email_Address'
            return jsonify(msg)
        elif patients_phone_number == '':
            msg = 'Please Input Phone_Number'
            return jsonify(msg)
        else:
            cur.execute(
                "UPDATE logininfo.patients SET patients_first_name = %s, patients_last_name = %s, Patients_father_name = %s,Patient_address = %s, Patients_email_address = %s, patients_phone_number = %s WHERE idPatients = %s ",
                [patients_f_name, patients_l_name, Patients_father_name, Patient_address, Patients_email_address,
                 patients_phone_number, string])
        db.connection.commit()
        cur.close()
        print(cur)
        msg = 'Record successfully Updated'
    return jsonify(msg)


# Delete User
# @app.route("/deleteUser/<string:id>",methods=['GET','POST'])
# def deleteUser(id):
# cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
# cur.execute("delete  from patients where idPatients=%s",([id],))
# db.connection.commit()
# cur.close()
# cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
# patients_RECORD = cursor.execute("SELECT * FROM patients ")
# patients_RECORD = cursor.execute("SELECT * FROM logininfo.patients WHERE patients_first_name=%s", ([patients]))
# """Api to retive all the patient from the database"""
# if (patients_RECORD) > 0:
# user_details = cursor.fetchall()
# print(user_details)
# db.connection.commit()
##return render_template("Patients.html", user_details=user_details)




# ********************   DOCTORS   *******************###

@app.route('/new/doctor', methods=['GET', 'POST'])
def dotor():

    if request.method == 'POST':
        if "doctors_first_name" in request.form and "doctors_last_name" in request.form and "doctors_Address" in request.form and "doctors_Qualification" in request.form and "doctor_email_Address_name" in request.form and "doctor_Phone_Number" in request.form and "doctor_Speciality" in request.form and "doctor_Gender" in request.form:
            doctors_first_name = request.form['doctors_first_name']
            doctors_last_name = request.form['doctors_last_name']
            doctors_Address = request.form['doctors_Address']
            doctors_Qualification = request.form['doctors_Qualification']
            doctor_email_Address_name = request.form['doctor_email_Address_name']
            doctor_Phone_Number = request.form['doctor_Phone_Number']
            doctor_Speciality = request.form['doctor_Speciality']
            doctor_Gender = request.form['doctor_Gender']
            # password = request.form['password'].encode("ascii")
            # encoded = base64.b64encode(password)
            # decoded = encoded.decode('ascii', 'strict')
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO logininfo.doctor(Doctor_First_Name,Doctors_Last_Name,Doctors_Address,Doctors_Email_Address,Doctors_Phone_Number,Doctors_Speciality,Doctors_Qualification,Doctors_Gender) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                (doctors_first_name, doctors_last_name, doctors_Address, doctors_Qualification, doctor_email_Address_name,
                 doctor_Phone_Number,doctor_Speciality,doctor_Gender))
            db.connection.commit()
            cursor.close()
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            doctor_RECORD = cursor.execute("SELECT * FROM doctor ")
            # patients_RECORD = cursor.execute("SELECT * FROM logininfo.patients WHERE patients_first_name=%s", ([patients]))
            """Api to retive all the doctor from the database"""
            if (doctor_RECORD ) > 0:
                user_details = cursor.fetchall()
                print(user_details)
                # db.connection.commit()
            return render_template("Doctor.html", doctor_details=user_details)
            # return render_template("pateints_record_register.html")
            # return redirect(url_for(''))
        # return redirect(url_for('get'))

    return render_template("Doctor.html")



@app.route("/ajax_update_doctor", methods=["POST", "GET"])
def doctor_update():
    if request.method == 'POST':
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        string = request.form['string']
        doctor_f_name = request.form['doctor_f_name']
        doctor_last_name = request.form['doctor_last_name']
        doctor_address = request.form['doctor_address']
        doctor_qualification = request.form['doctor_qualification']
        doctor_email_address = request.form['doctor_email_address']
        doctor_phone_number = request.form['doctor_phone_number']
        doctor_speciality = request.form['doctor_speciality']
        doctor_gender = request.form['doctor_gender']
        print(string)
        if doctor_f_name == '' and doctor_last_name == '' and doctor_address == '' and doctor_qualification == '' and doctor_email_address == '' and doctor_phone_number == '' and doctor_speciality =='' and doctor_gender =='':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif doctor_f_name == '':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif doctor_last_name == '':
            msg = 'Please Input Last_name'
            return jsonify(msg)
        elif doctor_address == '':
            msg = 'Please Input Address'
            return jsonify(msg)
        elif doctor_qualification == '':
            msg = 'Please Input Qualification'
            return jsonify(msg)
        elif doctor_email_address == '':
            msg = 'Please Input Email_Address'
            return jsonify(msg)
        elif doctor_phone_number == '':
            msg = 'Please Input Phone_Number'
            return jsonify(msg)
        elif doctor_speciality == '':
            msg = 'Please Input doctor_speciality'
            return jsonify(msg)
        elif doctor_gender == '':
            msg = 'Please Input doctor_gender'
            return jsonify(msg)
        else:
            cur.execute(
                "UPDATE logininfo.doctor SET Doctor_First_Name = %s, Doctors_Last_Name = %s, Doctors_Address = %s,Doctors_Qualification = %s,Doctors_Email_Address=%s, Doctors_Phone_Number = %s, Doctors_Speciality = %s,Doctors_Gender=%s WHERE idDoctor = %s ",
                [doctor_f_name, doctor_last_name, doctor_address,doctor_qualification, doctor_email_address,
                 doctor_phone_number,doctor_speciality,doctor_gender, string])
        db.connection.commit()
        cur.close()
        print(cur)

        msg = 'Record successfully Updated'
    return jsonify(msg)

@app.route("/ajax_delete_doctor", methods=["POST", "GET"])
def delete_doctor():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('delete  from doctor where idDoctor={0}'.format(getid))
        cur.execute('ALTER TABLE doctor AUTO_INCREMENT = 1')
        db.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


@app.route('/new/medicines', methods=["POST", "GET"])
def medicine():
    if request.method == 'POST':
        if "Med_code" in request.form and "Med_Name" in request.form and "Med_Brand" in request.form and "Med_description" in request.form:
            Med_code = request.form['Med_code']
            Med_Name = request.form['Med_Name']
            Med_Brand = request.form['Med_Brand']
            Med_description = request.form['Med_description']

            # password = request.form['password'].encode("ascii")
            # encoded = base64.b64encode(password)
            # decoded = encoded.decode('ascii', 'strict')
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO logininfo.medicines(Med_code,Med_Name,Med_Brand,Med_description)VALUES(%s,%s,%s,%s)",
                (Med_code, Med_Name, Med_Brand, Med_description,))
            db.connection.commit()
            cursor.close()
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            doctor_RECORD = cursor.execute("SELECT * FROM medicines ")
            # patients_RECORD = cursor.execute("SELECT * FROM logininfo.patients WHERE patients_first_name=%s", ([patients]))
            """Api to retive all the doctor from the database"""
            if (doctor_RECORD ) > 0:
                user_details = cursor.fetchall()
                print(user_details)
                # db.connection.commit()
            return render_template("Medicines.html", medicine_details=user_details)
            # return render_template("pateints_record_register.html")
            # return redirect(url_for(''))
        # return redirect(url_for('get'))

    return render_template("Medicines.html")



@app.route("/ajax_update_medicine", methods=["POST", "GET"])
def medicine_update():
    if request.method == 'POST':
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        string = request.form['string']
        Medicine_code = request.form['Medicine_code']
        Med_Name = request.form['Medicine_Name']
        Med_Brand = request.form['Medicine_Brand']
        Med_description = request.form['Medicine_description']

        print(string)
        print(Medicine_code)
        print(Med_description)
        print(Med_Brand)

        if Medicine_code == '' and Med_Name == '' and Med_Brand == '' and Med_description == '':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif Medicine_code == '':
            msg = 'Please Input first_name'
            return jsonify(msg)
        elif Med_Name == '':
            msg = 'Please Input Last_name'
            return jsonify(msg)
        elif Med_Brand == '':
            msg = 'Please Input Address'
            return jsonify(msg)
        elif Med_description == '':
            msg = 'Please Input Qualification'
            return jsonify(msg)

        else:
            cur.execute(
                "UPDATE  logininfo.medicines SET Med_code = %s, Med_Name = %s,Med_Brand = %s,Med_description=%s WHERE idmedicines = %s ",
                [Medicine_code, Med_Name, Med_Brand,Med_description, string])
        db.connection.commit()
        cur.close()
        print(cur)

        msg = 'Record successfully Updated'
    return jsonify(msg)

@app.route("/ajax_delete_medicine", methods=["POST", "GET"])
def delete_medicine():
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('delete  from medicines where idmedicines={0}'.format(getid))
        cur.execute('ALTER TABLE medicines AUTO_INCREMENT = 1')
        db.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)
