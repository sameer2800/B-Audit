from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from owner_registration import Owner
from contractor_registration import Contractor
from house_registration import House
from device_registration import Device
from service_registration import Service
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    if session.get('logged_in'):
        return redirect(url_for(session.get('type'), username = session.get('username')))
    else:
        return render_template("index.html")

@app.route('/owner-register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        form = request.form
        if form["password"] == form["retypepassword"]:
            engine = create_engine('sqlite:///owners.db', echo=True)
            Session = sessionmaker(bind=engine)
            db_session = Session()
            owner = Owner(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]))
            db_session.add(owner)
            db_session.commit()
            db_session.close()
            return redirect(url_for('owner_login'))
        else:
            return render_template("owner_register.html")
    else:
        return render_template("owner_register.html")

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST' and session.get('logged_in') is None:
        conn = sqlite3.connect('owners.db')
        cursor = conn.cursor()
        query = 'SELECT password from owners where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][0] == request.form["password"]:
            session['logged_in'] = True
            session['type'] = 'owner'
            session['username'] = request.form["username"]
            return redirect(url_for('owner', username = request.form["username"]))
        else:
            return render_template("owner_login.html")
    else:
        if session.get('logged_in'):
            return redirect(url_for('homepage'))
        else:
            return render_template("owner_login.html")

@app.route('/contractor-register', methods=['GET', 'POST'])
def contractor_register():
    if request.method == 'POST':
        form = request.form
        if form["password"] == form["retypepassword"]:
            engine = create_engine('sqlite:///contractors.db', echo=True)
            Session = sessionmaker(bind=engine)
            db_session = Session()
            contractor = Contractor(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]))
            db_session.add(contractor)
            db_session.commit()
            db_session.close()
            return redirect(url_for('contractor_login'))
        else:
            return render_template("contractor_register.html")
    else:
        return render_template("contractor_register.html")

@app.route('/contractor-login', methods=['GET', 'POST'])
def contractor_login():
    if request.method == 'POST' and session.get('logged_in') is None:
        conn = sqlite3.connect('contractors.db')
        cursor = conn.cursor()
        query = 'SELECT password from contractors where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][0] == request.form["password"]:
            session['logged_in'] = True
            session['type'] = 'contractor'
            session['username'] = request.form["username"]
            return redirect(url_for('contractor', username = request.form["username"]))
        else:
            return render_template("contractor_login.html")
    else:
        if session.get('logged_in'):
            return redirect(url_for('homepage'))
        else:
            return render_template("contractor_login.html")

@app.route('/owner/<username>', methods=['GET', 'POST'])
def owner(username):
    if session.get('username') == username and session.get('type') == 'owner':
        if request.method == 'POST':
            if isinstance(request.form.get("register_house"), unicode):
                engine = create_engine('sqlite:///houses.db', echo=True)
                Session = sessionmaker(bind=engine)
                db_session = Session()
                house = House(str(username), str(request.form["name"]), str(request.form["location"]))
                db_session.add(house)
                db_session.commit()
                db_session.close()
            elif isinstance(request.form.get("cancel_service"), unicode):
                conn = sqlite3.connect('services.db')
                cursor = conn.cursor()
                query = 'DELETE from services where id = \''+str(request.form["id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()

        conn = sqlite3.connect('houses.db')
        cursor = conn.cursor()
        query = 'SELECT * from houses where owner = \''+str(username)+'\''
        houses = cursor.execute(query).fetchall()
        cursor.close()

        conn = sqlite3.connect('services.db')
        cursor = conn.cursor()

        query = 'SELECT * from services where owner = \''+str(username)+'\' and status = "need"'
        applied_services = cursor.execute(query).fetchall()

        query = 'SELECT * from services where owner = \''+str(username)+'\' and status = "taken"'
        ongoing_services = cursor.execute(query).fetchall()

        cursor.close()

        return render_template("owner.html", username = username, houses = houses, applied_services = applied_services, ongoing_services = ongoing_services)
    else:
        return redirect(url_for('homepage'))

@app.route('/contractor/<username>', methods=["GET", "POST"])
def contractor(username):
    if session.get('username') == username and session.get('type') == 'contractor':
        conn = sqlite3.connect('services.db')
        cursor = conn.cursor()

        if request.method == "POST":
            if isinstance(request.form.get("done"), unicode):
                query = 'UPDATE services SET contractor = \''+session.get("username")+'\', status = "done" WHERE id = \''+request.form["id"]+'\''
                cursor.execute(query)
                conn.commit()
            elif isinstance(request.form.get("remove"), unicode):
                query = 'UPDATE services SET contractor = "None", status = "need" WHERE id = \''+request.form["id"]+'\''
                cursor.execute(query)
                conn.commit()

        query = 'SELECT * from services where contractor = \''+str(username)+'\' and status = "taken"'
        ongoing_services = cursor.execute(query).fetchall()

        query = 'SELECT * from services where contractor = \''+str(username)+'\' and status = "done"'
        done_services = cursor.execute(query).fetchall()

        cursor.close()
        return render_template("contractor.html", ongoing_services = ongoing_services, done_services = done_services)
    else:
        return redirect(url_for('homepage'))

@app.route('/house/<number>', methods=['GET', 'POST'])
def house(number):
    conn = sqlite3.connect('houses.db')
    cursor = conn.cursor()
    query = 'SELECT owner from houses where id = \''+str(number)+'\''
    result = cursor.execute(query).fetchall()
    cursor.close()

    if (result[0][0] == session.get('username') and session.get('type') == 'owner'):
        if request.method == 'POST':
            if isinstance(request.form.get("register_device"), unicode):
                engine = create_engine('sqlite:///devices.db', echo=True)
                Session = sessionmaker(bind=engine)
                db_session = Session()
                device = Device(str(request.form["name"]), int(number), "working")
                db_session.add(device)
                db_session.commit()
                db_session.close()
            elif isinstance(request.form.get("register_service"), unicode):
                engine = create_engine('sqlite:///services.db', echo=True)
                Session = sessionmaker(bind=engine)
                db_session = Session()
                device = Service(session.get('username'), int(number), int(request.form["device_id"]), 'None', str(request.form["type"]), str(request.form["cost"]), "need")
                db_session.add(device)
                db_session.commit()
                db_session.close()
            elif isinstance(request.form.get("cancel_service"), unicode):
                conn = sqlite3.connect('services.db')
                cursor = conn.cursor()
                query = 'DELETE from services where id = \''+str(request.form["id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()

        conn = sqlite3.connect('devices.db')
        cursor = conn.cursor()
        query = 'SELECT * from devices where house_id = \''+str(number)+'\''
        devices = cursor.execute(query).fetchall()
        cursor.close()

        conn = sqlite3.connect('services.db')
        cursor = conn.cursor()

        query = 'SELECT * from services where house_id = \''+str(number)+'\' and status = "need"'
        applied_services = cursor.execute(query).fetchall()

        query = 'SELECT * from services where house_id = \''+str(number)+'\' and status = "taken"'
        ongoing_services = cursor.execute(query).fetchall()

        cursor.close()
        return render_template("house.html", username = session.get("username"), number = number, devices = devices, applied_services = applied_services, ongoing_services = ongoing_services)
    else:
        return redirect(url_for('homepage'))

@app.route('/marketplace', methods = ['GET', 'POST'])
def marketplace():
    if not session.get('logged_in'):
        return redirect(url_for('homepage'))

    conn = sqlite3.connect('services.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        query = 'UPDATE services SET contractor = \''+session.get("username")+'\', status = "taken" WHERE id = \''+request.form["id"]+'\''
        cursor.execute(query)
        conn.commit()

    query = 'SELECT * from services where status = "need"'
    need_services = cursor.execute(query).fetchall()

    query = 'SELECT * from services where status = "taken"'
    ongoing_services = cursor.execute(query).fetchall()

    cursor.close()
    return render_template("marketplace.html", type = session.get("type"), username = session.get("username"), need_services = need_services, ongoing_services = ongoing_services)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
