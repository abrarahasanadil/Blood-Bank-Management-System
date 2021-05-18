from flask import Blueprint, render_template, request, redirect, flash, session
from flask.helpers import url_for
from flask_login.utils import login_required, current_user

from . import DB_NAME, db
import sqlite3
import os.path

datadir = '/home/abrarahasanadil/vscode_Projects/blood_bank_database/website/bloodbank.db'

views = Blueprint('views', __name__)

# ? WILL RUN WHEN WE GO TO THE / ROUTE


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


# ! ----------------------------------------------------------------DASH
@views.route('/dashboard')
@login_required
def dashboard():
    connection = sqlite3.connect(datadir)
    c = connection.cursor()
    c.execute("SELECT COUNT(*) FROM user")
    data = c.fetchall()
    c.close()
    connection.commit()

    i = 0
    for i in data:
        i = list(i)
        i = i[0]

    return render_template("dashboard.html", user=current_user, name=current_user.name, count=i)


# ! ----------------------------------------------------------------DOCTORS
@views.route('/doctors')
@login_required
def doctors():
    connection = sqlite3.connect(datadir)
    c = connection.cursor()
#    c.execute('''INSERT INTO doctor (name, phone)
#                VALUES
#                ("Dr. Sheikh", "01612345098"),
#                ("Dr. Nazia", "01723447098"),
#                ("Dr. Adil", "01898234099"),
#                ("Dr. Kazi", "01323987611"),
#                ("Dr. Rafid", "01633987611"),
#                ("Dr. Sababa", "01923107611"),
#                ("Dr. Bushra", "01723987888"),
#                ("Dr. Mahi", "01923945678")
#                ''')
    c.execute("SELECT * FROM doctor")
    data = c.fetchall()
    c.close()
    connection.commit()

    return render_template("doctors.html", user=current_user, doc=data)


# ! ----------------------------------------------------------------BANK
@views.route('/bloodbanks')
@login_required
def bloodbanks():
    connection = sqlite3.connect(datadir)
    c = connection.cursor()

#    c.execute('''INSERT INTO bloodbank (name, address)
#                VALUES
#                ("Life Save Blood Bank", "O.R. Nizam Rd, Chattogram"),
#                ("Fatema Begum Red Crescent Blood Center", "395 Kata Pahar Ln, Chattogram"),
#                ("Blood Bank - Bangladesh Red Crescent Society", "7, 5 Aurangajeb Rd, Dhaka"),
#                ("Unique Blood Bank & Transfusion Center", "Chittagong - Khagrachhari Rd, Hathazari"),
#                ("Sitakund blood bank", "Sitakund"),
#                ("Quantum Blood Lab", "31/V Shilpacharya Zainul Abedin Sarak, Shantinagar, Dhaka 1217"),
#                ("Crescent Blood Bank", "Dorgah Moholla Rd, Sylhet 3100"),
#                ("Rajshahi Blood Bank and Transfusion Center", "Holding no 106, Rajshahi 6100")
#                ''')
    c.execute("SELECT * FROM bloodbank")
    data = c.fetchall()
    c.close()
    connection.commit()

    return render_template("bloodbanks.html", user=current_user, bb=data)


# ! ----------------------------------------------------------------STOCKS
@views.route('/bloodstocks',  methods=['POST', 'GET'])
@login_required
def bloodstocks():
    connection = sqlite3.connect(datadir)
    c = connection.cursor()
#    c.execute('''INSERT INTO blood (blood_type, donor_id, bloodbank_id)
#                VALUES
#                ((SELECT blood_type from user WHERE id='5'), (SELECT id from user WHERE id='5'), (SELECT id from bloodbank WHERE id='1')),
#                ((SELECT blood_type from user WHERE id='3'), (SELECT id from user WHERE id='3'), (SELECT id from bloodbank WHERE id='6')),
#                ((SELECT blood_type from user WHERE id='4'), (SELECT id from user WHERE id='4'), (SELECT id from bloodbank WHERE id='2')),
#                ((SELECT blood_type from user WHERE id='2'), (SELECT id from user WHERE id='2'), (SELECT id from bloodbank WHERE id='3')),
#                ((SELECT blood_type from user WHERE id='6'), (SELECT id from user WHERE id='6'), (SELECT id from bloodbank WHERE id='4')),
#                ((SELECT blood_type from user WHERE id='1'), (SELECT id from user WHERE id='1'), (SELECT id from bloodbank WHERE id='1'))
#                ''')

    c.execute("SELECT * FROM blood")
    data = c.fetchall()
    c.close()
    connection.commit()

    if request.method == 'POST':
        donor_id = request.form.get('donor_id')
        session['donor_id'] = donor_id

        blood_id = request.form.get('blood_id')
        session['blood_id'] = blood_id

        blood_type = request.form.get('blood_type')
        session['blood_type'] = blood_type

        bloodtype = request.form.get('bloodtype')
        session['bloodtype'] = bloodtype

        if blood_type.upper() != bloodtype:
            flash(
                "Transfusion Requires Same Blood Type, Try different Option", category='error')
            return render_template("bloodstocks.html", user=current_user, bs=data)

        return redirect(url_for('views.blooddelivery'))

    return render_template("bloodstocks.html", user=current_user, bs=data)


# ! ----------------------------------------------------------------DELIVERY
@views.route('/blooddelivery')
@login_required
def blooddelivery():
    donor_id = session['donor_id']
    blood_id = session['blood_id']
    blood_type = session['blood_type']
    bloodtype = session['bloodtype']

    connection = sqlite3.connect(datadir, check_same_thread=False)
    connection.text_factory = sqlite3.OptimizedUnicode
    c = connection.cursor()
    c.execute(f'''INSERT INTO blooddelivery(patient_id, bloodbank_id)
                VALUES
                ((SELECT id FROM user WHERE id = '{current_user.id}'), (SELECT bloodbank_id FROM blood WHERE bloodbank_id = '{blood_id}'))
                ''')

    data = c.execute(f"SELECT * FROM blooddelivery WHERE id='{blood_id}'")

    data = c.fetchall()
    c.close()

    return render_template("blooddelivery.html", user=current_user, bd=data)


# ! ----------------------------------------------------------------PROFILE
@views.route('/account')
@login_required
def account():
    connection = sqlite3.connect(datadir, check_same_thread=False)
    connection.text_factory = sqlite3.OptimizedUnicode
    c = connection.cursor()
    c.execute(f"SELECT * FROM user WHERE id = '{current_user.id}'")

    data = c.fetchall()
    c.close()

    return render_template("account.html", user=current_user, account=data)
