from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os
import mysql.connector

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'D:\Documents\Python\Py-project-IV'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/vehicle', methods=['POST'])
def vehicle():
    username = request.form['username']
    v_name = request.form['v_name']
    model = request.form['model']
    load_capacity = request.form['load-capacity']
    contact = request.form['contact']
    f_t = request.form['f_t']
    driver_license = request.form['driver-license']
    other_details = request.form['other-details']

    vehicle_registration = request.files['vehicle-registration']
    insurance_document = request.files['insurance-document']

    if vehicle_registration and allowed_file(vehicle_registration.filename):
        filename = secure_filename(vehicle_registration.filename)
        vehicle_registration.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if insurance_document and allowed_file(insurance_document.filename):
        filename = secure_filename(insurance_document.filename)
        insurance_document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                  host='localhost',
                                  database='tms')
    cursor = cnx.cursor()
    query = "INSERT INTO vehicles(username,v_name, model, load_capacity, contact, f_t, driver_license, other_details) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (username,v_name, model, load_capacity, contact, f_t, driver_license, other_details)

    cursor.execute(query, data)

    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect('/landing')




@app.route('/landing', methods=['GET'])
def landing():
    search_query = request.args.get('search')
    
    cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                  host='localhost',
                                  database='tms')
    cursor = cnx.cursor()
    
    if search_query:
        query = "SELECT * FROM vehicles WHERE f_t = %s"
        cursor.execute(query, (search_query,))
    else:
        query = "SELECT * FROM vehicles"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    
    column_names = [i[0] for i in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    
    cursor.close()
    cnx.close()
    
    return render_template('landing.html', data=data)



@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    contact = request.form.get('contact')

    insert_data(name, username, password, confirm_password, contact)

    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if validate_login(username, password):
        return redirect('/landing')
    else:
        return 'Invalid username or password.'

def insert_data(name, username, password, confirm_password, contact):
    try:
        cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                      host='localhost',
                                      database='tms')

        cursor = cnx.cursor()

        query = ("INSERT INTO your_table "
                 "(name, username, password, confirm_password, contact) "
                 "VALUES (%s, %s, %s, %s, %s)")

        cursor.execute(query, (name, username, password, confirm_password, contact))

        cnx.commit()

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")

def validate_login(username, password):
    try:
        cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                      host='localhost',
                                      database='tms')

        cursor = cnx.cursor()

        query = ("SELECT * FROM your_table WHERE username = %s AND password = %s")

        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        cursor.close()
        cnx.close()

        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return False

@app.route('/book', methods=['POST'])
def book():
    username = request.form['username']
    v_name = request.form['v_name']
    contact = request.form['contact']
    tons = request.form['tons']
    date = request.form['date']

    print(f"Username: {username}")
    print(f"Vehicle Name: {v_name}")

    cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                  host='localhost',
                                  database='tms')
    cursor = cnx.cursor()
    query = "INSERT INTO orders(username, v_name, contact, tons, date) VALUES(%s, %s, %s, %s, %s)"
    data = (username, v_name, contact, tons, date)

    cursor.execute(query, data)

    cnx.commit()
    cursor.close()
    cnx.close()

    return render_template('landing.html', username=username, v_name=v_name)

@app.route('/check_booking', methods=['GET', 'POST'])
def check_booking():
    if request.method == 'POST':
        username = request.form['username']
        v_name = request.form['v_name']

        cnx = mysql.connector.connect(user='root', password='Bharath@2004',
                                      host='localhost',
                                      database='tms')
        cursor = cnx.cursor()

        query = "SELECT * FROM orders WHERE username = %s AND v_name = %s"
        cursor.execute(query, (username, v_name))

        rows = cursor.fetchall()

        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]

        cursor.close()
        cnx.close()

        return render_template('booking_details.html', data=data)

    return render_template('check_booking.html')


if __name__ == '__main__':
    app.run(debug=True)