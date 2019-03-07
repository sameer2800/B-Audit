from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from owner_registration import Owner
from contractor_registration import Contractor
from house_registration import House
from device_registration import Device
from service_registration import Service
import base64
import re
import sqlite3
import os
import random
import string
import ed25519

from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TSocket import TSocket
import base58
from api.API import Client

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
            signing_key, verifying_key = ed25519.create_keypair()
            open(form["username"] + "-B-Audit-owner-key","wb").write(signing_key.to_bytes())
            vkey_hex = verifying_key.to_ascii(encoding="hex")
            engine = create_engine('sqlite:///owners.db', echo=True)
            Session = sessionmaker(bind=engine)
            db_session = Session()
            owner = Owner(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]), vkey_hex)
            db_session.add(owner)
            db_session.commit()
            db_session.close()
            print("New account generated!!! With wallet: " + str(vkey_hex))
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
        query = 'SELECT wallet, password from owners where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][1] == request.form["password"]:
            session['logged_in'] = True
            session['type'] = 'owner'
            session['username'] = request.form["username"]
            session['wallet'] = result[0][0]
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
            signing_key, verifying_key = ed25519.create_keypair()
            open(form["username"] + "-B-Audit-contractor-key","wb").write(signing_key.to_bytes())
            vkey_hex = verifying_key.to_ascii(encoding="hex")
            engine = create_engine('sqlite:///contractors.db', echo=True)
            Session = sessionmaker(bind=engine)
            db_session = Session()
            contractor = Contractor(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]), vkey_hex)
            db_session.add(contractor)
            db_session.commit()
            db_session.close()
            print("New account generated!!! With wallet: " + str(vkey_hex))
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
        query = 'SELECT wallet, password from contractors where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][1] == request.form["password"]:
            session['logged_in'] = True
            session['type'] = 'contractor'
            session['username'] = request.form["username"]
            session['wallet']  = result[0][0]
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
                data = re.sub('^data:image/.+;base64,', '', request.form['houseimage'])
                binary_data = base64.b64decode(data)
                imagename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + ".jpg"
                fd = open('./static/images/house_images/' + imagename, 'wb')
                fd.write(binary_data)
                fd.close()

                engine = create_engine('sqlite:///houses.db', echo=True)
                Session = sessionmaker(bind=engine)
                db_session = Session()
                house = House(str(username), str(request.form["name"]), str(request.form["location"]), imagename)
                db_session.add(house)
                db_session.commit()
                db_session.close()
            elif isinstance(request.form.get("cancel_house"), unicode):
                conn = sqlite3.connect('houses.db')
                cursor = conn.cursor()
                query = 'DELETE from houses where id = \''+str(request.form["house_id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()

                conn = sqlite3.connect('devices.db')
                cursor = conn.cursor()
                query = 'DELETE from devices where house_id = \''+str(request.form["house_id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()

                conn = sqlite3.connect('services.db')
                cursor = conn.cursor()
                query = 'DELETE from services where house_id = \''+str(request.form["house_id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()
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

        balance = 0

        return render_template("owner.html", username = username, wallet = session['wallet'], balance = balance, houses = houses, applied_services = applied_services, ongoing_services = ongoing_services)
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

        balance = 0

        return render_template("contractor.html", ongoing_services = ongoing_services, done_services = done_services, username = username, wallet = session['wallet'], balance = balance)
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
                data = re.sub('^data:image/.+;base64,', '', request.form['deviceimage'])
                binary_data = base64.b64decode(data)
                imagename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + ".jpg"
                fd = open('./static/images/device_images/' + imagename, 'wb')
                fd.write(binary_data)
                fd.close()

                engine = create_engine('sqlite:///devices.db', echo=True)
                Session = sessionmaker(bind=engine)
                db_session = Session()
                device = Device(str(request.form["name"]), int(number), "working", imagename)
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
            elif isinstance(request.form.get("cancel_device"), unicode):
                conn = sqlite3.connect('devices.db')
                cursor = conn.cursor()
                query = 'DELETE from devices where id = \''+str(request.form["device_id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()

                conn = sqlite3.connect('services.db')
                cursor = conn.cursor()
                query = 'DELETE from services where device_id = \''+str(request.form["device_id"])+'\''
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

@app.route('/house-registration', methods = ['GET', 'POST'])
def house_registration():
    if session.get('logged_in') == True and session.get('type') == 'owner':
        if request.method == 'POST':
            return redirect(url_for('homepage'))
        else:
            return render_template("house_registration.html")
    else:
        return redirect(url_for('homepage'))

@app.route('/device-registration', methods = ['GET', 'POST'])
def device_registration():
    if session.get('logged_in') == True and session.get('type') == 'owner':
        if request.method == 'POST':
            return redirect(url_for('homepage'))
        else:
            return render_template("device_registration.html")
    else:
        return redirect(url_for('homepage'))

@app.route('/service-registration', methods = ['GET', 'POST'])
def service_registration():
    if session.get('logged_in') == True and session.get('type') == 'owner':
        if request.method == 'POST':
            return redirect(url_for('homepage'))
        else:
            return render_template("service_registration.html")
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
    app.run(debug=False)
