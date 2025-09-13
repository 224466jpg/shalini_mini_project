from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '12/12=1shals'
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12/12=1shals",
    database="company"
)
cursor = db.cursor(dictionary=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            return redirect('/login')
        except mysql.connector.IntegrityError:
            return "Email already exists. Try logging in."
        
    return render_template("register.html")

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect('/employee-details')
        else:
            return "Invalid email or password"

    return render_template("login.html")

# Employee Details page
@app.route('/employee-details', methods=['GET', 'POST'])
def employee_details():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['empName']
        emp_id = request.form['empId']
        dept = request.form['empDept']
        email = request.form['empEmail']

        cursor.execute("INSERT INTO employees (name, employee_id, department, email) VALUES (%s, %s, %s, %s)",
                    (name, emp_id, dept, email))
        db.commit()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    return render_template("employee-details.html", employees=employees)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

# Run app
if __name__ == '__main__':
    app.run(debug=True)
