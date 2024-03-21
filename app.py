from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'
mysql = MySQL(app)

# Registration Form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request)
        userDetails = request.form
        username = userDetails.get('name' )
        password = userDetails['password']
        email = userDetails.get('Email' )
        mobile = userDetails.get('mobile' )

        cursor = mysql.connection.cursor()
        print(username)
        cursor.execute("INSERT INTO tbl_users (username, password,Email,Name) VALUES(%s, %s,%s,%s)", (mobile, password,email,username))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['mobile']
        password = userDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Login failed. Please check your username and password.'
    return render_template('login.html')

# Dashboard
@app.route('/dashborad')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
