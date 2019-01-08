from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/owner-register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        return redirect(url_for('owner_login'))
    else:
        return render_template("owner_register.html")

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        return redirect(url_for('owner'))
    else:
        return render_template("owner_login.html")

@app.route('/contractor-register', methods=['GET', 'POST'])
def contractor_register():
    if request.method == 'POST':
        return redirect(url_for('contractor_login'))
    else:
        return render_template("contractor_register.html")

@app.route('/contractor-login', methods=['GET', 'POST'])
def contractor_login():
    if request.method == 'POST':
        return redirect(url_for('contractor'))
    else:
        return render_template("contractor_login.html")
@app.route('/owner')
def owner():
    return render_template("owner.html")

@app.route('/contractor')
def contractor():
    return render_template("contractor.html")

@app.route('/house')
def house():
    return render_template("house.html")

@app.route('/marketplace')
def marketplace():
    return render_template("marketplace.html")


if __name__ == "__main__":
    app.run(debug=True)
