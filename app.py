from flask import Flask, session, flash, redirect, url_for, escape, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from wtforms import validators
import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.apps import custom_app_context as pwd_context
from random import randint
import random
import pyautogui
import json



app = Flask(__name__)

# Initialize Form For Credentials
class authForm(FlaskForm): 
    enrollmentID = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enrollment ID"})
    #dept = StringField(validators=[DataRequired()], render_kw={"placeholder": "Department"})

#Initialize Form For voter Enrollment
class enrollmentForm(FlaskForm):
    firstName = StringField(validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    matricNo = StringField(validators=[DataRequired()], render_kw={"placeholder": "Reg Number"})
    
class candidateForm(FlaskForm):
    firstName = StringField(validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    matricNo = StringField(validators=[DataRequired()], render_kw={"placeholder": "Reg Number"})

    
#Initialize Form For Login
class loginForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Admin ID"})
        

# Database Configurations
conn = MySQLdb.connect(host="localhost", 
                    user="root", 
                    passwd="jccofficial", 
                    db="test")
cur = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voter-login',methods=["GET", "POST"])
def voterLogin():
    form = authForm()
    if 'enrollmentID' in session:
        return redirect(url_for('votingPortal'))
    elif request.method == 'GET':
        return render_template('voter-login.html', form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit() or request.form['enrollmentID'] == "":
            flash('All fields are required.')
            return render_template('voter-login.html', form=form)
        enrollmentID  = request.form['enrollmentID']
        #dept = request.form.get('select_dept')
        #return(str(dept))
        data = cur.execute(
                """SELECT * FROM voters WHERE uniqueid = (%s)""", [enrollmentID]) # CHECKS IF USERNAME EXSIST
        data = cur.fetchone()
        if data:
            session['enrollmentID'] = request.form['enrollmentID']
            return redirect(url_for('votingPortal'))
        else:
            flash("Invalid Credential")
            return render_template('voter-login.html', form=form)

@app.route('/voting-portal')
def votingPortal():
    if 'enrollmentID' in session:
        
        presidentialCandidates = cur.execute(
                """SELECT firstname FROM candidates WHERE post='President'""") # SELECTS ALL PRESIDENTIAL CANDIDATES
        presidentialCandidates = cur.fetchall()
        presidentialCandidatesList = [] 
        if presidentialCandidates:
            for candidate in presidentialCandidates:
                presidentialCandidatesList.append(str(candidate).strip("'(,)''"))
            print(presidentialCandidatesList)
        elif presidentialCandidates == ():
            presidentialCandidatesList.append("No Records Found in Database")
        
        vicePresidentialCandidates = cur.execute(
                """SELECT firstname FROM candidates WHERE post='Vice President'""") # SELECTS ALL VICE CANDIDATES
        vicePresidentialCandidates = cur.fetchall()
        vicePresidentialCandidatesList = [] 
        if vicePresidentialCandidates:
            for candidate in vicePresidentialCandidates:
                vicePresidentialCandidatesList.append(str(candidate).strip("'(,)''"))
        elif vicePresidentialCandidates == ():
            vicePresidentialCandidatesList.append("No Records Found in Database")

        finsecCandidates = cur.execute(
                """SELECT firstname FROM candidates WHERE post='Finacial Secreatary'""") # SELECTS ALL FINSEC CANDIDATES
        finsecCandidates = cur.fetchall()
        finsecCandidatesList = [] 
        if finsecCandidates:
            for candidate in finsecCandidates:
                finsecCandidatesList.append(str(candidate).strip("'(,)''"))
        elif finsecCandidates == ():
            finsecCandidatesList.append("No Records Found in Database")
        return render_template('voting-portal.html',finsecCandidates=finsecCandidatesList,vicePresidentialCandidates=vicePresidentialCandidatesList, presidentialCandidates=presidentialCandidatesList, data=session['enrollmentID'])
    return redirect(url_for('voterLogin'))

@app.route('/enroll-voter', methods=['GET', 'POST'])
def enrollVoter():
    form = enrollmentForm()
    form2 = candidateForm()
    if 'password' not in session:
        return redirect(url_for('adminLogin'))
    elif request.method == 'GET':
        return render_template('enroll.html', form=form2, dept=[{'name':'Department'}, {'name':'Chemistry'}, {'name':'Project Management Technology'}, {'name':'Computer Science'}], level=['300'], postVying=['Select Post','President','Vice President','Finacial Secreatatry', 'Welfare'])
    elif request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('enroll.html',form=form2, level=['300'], postVying=['Select Post','President','Vice President','Finacial Secreatatry', 'Welfare'], dept=[{'name':'Department'}, {'name':'Chemistry'}, {'name':'Project Management Technology'}, {'name':'Computer Science'}])
        try:
            firstName  = request.form['firstName']
            print(firstName)
            lastName  = request.form['lastName']
            print(lastName)
            matricNo = request.form['matricNo']
            print(matricNo)
            dept = request.form.get('select_dept')
            print(dept)
            uniqueID = generate_numbers("voter")
            print(uniqueID)
            check = cur.execute(
                """SELECT * FROM voters WHERE regnumber = (%s)""", [matricNo]) # CHECKS IF USERNAME EXSIST
            check = cur.fetchone()
            if check:
                return 'voter Already Exists'
            else:
                data = cur.execute(
                        """INSERT INTO voters (firstname, lastname, regnumber, dept, uniqueID)
                        VALUES (%s,%s,%s,%s,%s)""" ,(firstName, lastName, matricNo, dept, uniqueID))# Update Voters table.
                conn.commit()
                return render_template('receipt.html', firstName=firstName, uniqueID=uniqueID)
        except Exception as e:
            flash(str(e))
            return render_template('enroll.html', form=form2, postVying=[{'name':'President'}, {'name':'Vice President'}, {'name':'Finacial Secreatatry'}, {'name':'Welfare'}], dept=[{'name':'Department'}, {'name':'Chemistry'}, {'name':'Project Management Technology'}, {'name':'Computer Science'}])

@app.route('/enroll-candidate', methods=['GET', 'POST'])
def enrollCandidate():
    form = candidateForm()
    if 'password' not in session:
        return redirect(url_for('adminLogin'))
    elif request.method == 'GET':
        return render_template('enroll.html', form=form, dept=[{'name':'Department'}, {'name':'Chemistry'}, {'name':'Project Management Technology'}, {'name':'Computer Science'}], postVying=[{'name':'President'}, {'name':'Vice President'}, {'name':'Finacial Secreatatry'}, {'name':'Welfare'}] )
    elif request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('enroll.html',form=form, postVying=[{'name':'President'}, {'name':'Vice President'}, {'name':'Finacial Secreatatry'}, {'name':'Welfare'}])
        try:
            firstName  = request.form['firstName']
            print(firstName)
            lastName  = request.form['lastName']
            dept = request.form.get('select_dept')
            level  = request.form.get('select_level')
            postVying = request.form.get('select_post')
            print(postVying) 
            matricNo = request.form['matricNo']
            uniqueID = generate_numbers("candidate")
            print(uniqueID)
            check = cur.execute(
                """SELECT * FROM candidates WHERE regnumber = (%s)""", [matricNo]) # CHECKS IF USERNAME EXSIST
            check = cur.fetchone()
            if check:
                return 'Candidate Already Exists'
            else:
                data = cur.execute(
                        """INSERT INTO candidates (firstname, lastname, dept, level, post, regnumber, uniqueID)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)""" ,(firstName, lastName,dept, level, postVying, matricNo, uniqueID))# Update candidates table.
                conn.commit()
                return render_template('candidate.html', firstName=firstName, uniqueID=uniqueID)
        except Exception as e:
            flash(str(e))
            return render_template('enroll.html',form=form, postVying=[{'name':'President'}, {'name':'Vice President'}, {'name':'Finacial Secreatatry'}, {'name':'Welfare'}])
  
@app.route('/admin-login', methods=["GET", "POST"])
def adminLogin():
    form = loginForm()
    if 'password' in session:
        return redirect(url_for('enrollVoter'))
    elif request.method == 'GET':
        return render_template('admin-login.html', form=form)
    else:
        if not form.validate_on_submit() or request.form['password'] == "":
            flash('All fields are required.')
            return render_template('admin-login.html',form=form)
        password  = request.form['password']
        data = cur.execute(
                """SELECT * FROM admins WHERE adminid = (%s)""", [password]) # CHECKS IF ADMIN ID EXISTS
        data = cur.fetchone()
        if data:
            session['password'] = request.form['password']
            return redirect(url_for('enrollVoter'))
        else:
            flash("Invalid Credential")
            return render_template('admin-login.html',form=form)
    
@app.route('/update-vote', methods=["POST"])
def updateVotes():
    result = []
    data = request.get_json()
    voter = data['theVoter']
    candidate = data['theCandidate']
    post = data['thePost']
    result = [voter, candidate, post]
    voterID = result[0]
    candidate = result[1]
    post = post[32:]
    print(result) 
    try:
        data = cur.execute(
                    """INSERT INTO votes (voterid, candidateid, post)
                    VALUES (%s,%s,%s)""" ,(voterID, candidate, post))# Update votes table. 
        conn.commit()  
        return json.dumps({"status":"OK"})
    except Exception as e:
        return json.dumps({str(e):"Exception"})

def getCandidates():
    presidentialCandidates = cur.execute(
                """SELECT firstname, post FROM candidates WHERE post='President'""") # SELECTS ALL PRESIDENTIAL CANDIDATES
    presidentialCandidates = cur.fetchall()
    presidentialDict = {"names" :[ x[0] for x in presidentialCandidates], "post" : [x[1] for x in presidentialCandidates]}


    vicePresidentialCandidates = cur.execute(
                """SELECT firstname, post FROM candidates WHERE post='vice President'""") # SELECTS ALL VICE CANDIDATES
    vicePresidentialCandidates = cur.fetchall()
    vicePresidentialDict = {"names" :[ x[0] for x in vicePresidentialCandidates], "post" : [x[1] for x in vicePresidentialCandidates]}

    finsecCandidates = cur.execute(
                """SELECT firstname, post FROM candidates WHERE post='Finacial Secreatatry'""") # SELECTS ALL FINSEC CANDIDATES
    finsecCandidates = cur.fetchall()
    finsecDict = {"names" :[ x[0] for x in finsecCandidates], "post" : [x[1] for x in finsecCandidates]}

    return jsonify(presidentialDict,vicePresidentialDict,finsecDict)
@app.route('/api/v1/candidates/all')
def loadCandidates():
    return getCandidates()

@app.route('/logout')
def logout():
    session.pop('enrollmentID', None)
    return redirect(url_for('voterLogin'))

@app.route('/admin-logout')
def adminLogout():
    session.pop('password', None)
    return redirect(url_for('adminLogin'))

def generate_numbers(position):
    """ returns the formated serials """
    position = str(position)
    if position == "voter":
        serials = ''.join(str(random.randint(0,9)) for _ in range(6))
        return serials
    elif position == "candidate":
        serials = ''.join(str(random.randint(0,9)) for _ in range(8))
        return serials   


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run(debug=True)
