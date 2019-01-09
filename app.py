from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from owner_registration import Owner
from contractor_registration import Contractor
import sqlite3

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/owner-register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        form = request.form
        if form["password"] == form["retypepassword"]:
            engine = create_engine('sqlite:///owners.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            owner = Owner(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]))
            session.add(owner)
            session.commit()
            session.close()
            return redirect(url_for('owner_login'))
        else:
            return render_template("owner_register.html")
    else:
        return render_template("owner_register.html")

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        conn = sqlite3.connect('owners.db')
        cursor = conn.cursor()
        query = 'SELECT password from owners where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][0] == request.form["password"]:
            return redirect(url_for('owner', username = request.form["username"]))
        else:
            return render_template("owner_login.html")
    else:
        return render_template("owner_login.html")

@app.route('/contractor-register', methods=['GET', 'POST'])
def contractor_register():
    if request.method == 'POST':
        form = request.form
        if form["password"] == form["retypepassword"]:
            engine = create_engine('sqlite:///contractors.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            contractor = Contractor(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]))
            session.add(contractor)
            session.commit()
            session.close()
            return redirect(url_for('contractor_login'))
        else:
            return render_template("contractor_register.html")
    else:
        return render_template("contractor_register.html")

@app.route('/contractor-login', methods=['GET', 'POST'])
def contractor_login():
    if request.method == 'POST':
        conn = sqlite3.connect('owners.db')
        cursor = conn.cursor()
        query = 'SELECT password from contractors where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][0] == request.form["password"]:
            return redirect(url_for('contractor', username = request.form["username"]))
        else:
            return render_template("contractor_login.html")
    else:
        return render_template("contractor_login.html")

@app.route('/owner/<username>')
def owner(username):
    conn = sqlite3.connect('houses.db')
    cursor = conn.cursor()
    query = 'SELECT * from houses where owner = \''+str(username)+'\''
    result = cursor.execute(query).fetchall()
    cursor.close()
    return render_template("owner.html", houses = result)

@app.route('/contractor/<username>')
def contractor(username):
    conn = sqlite3.connect('services.db')
    cursor = conn.cursor()
    query = 'SELECT * from services where contractor = \''+str(username)+'\''
    result = cursor.execute(query).fetchall()
    cursor.close()
    return render_template("contractor.html", services = result)

@app.route('/house')
def house():
    return render_template("house.html")

@app.route('/marketplace')
def marketplace():
    conn = sqlite3.connect('services.db')
    cursor = conn.cursor()
    query = 'SELECT * from services where status = need'
    result = cursor.execute(query).fetchall()
    cursor.close()
    return render_template("marketplace.html")


if __name__ == "__main__":
    app.run(debug=True)