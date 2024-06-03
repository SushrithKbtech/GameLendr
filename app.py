from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('C:/Users/sushr/Downloads/user.db')
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a table to store user details
def create_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT,
                            last_name TEXT,
                            phone_number TEXT,
                            email TEXT,
                            username TEXT,
                            password TEXT)''')
        conn.commit()
        conn.close()

# Create table when the app starts
create_table()

# Function to create a table to store device/game details
def create_device_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            description TEXT,
                            cost INTEGER,
                            stock INTEGER)''')
        conn.commit()
        conn.close()

# Create table for devices when the app starts
create_device_table()
def add_initial_devices():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        devices = [
            ("Assassin's Creed Valhalla", "Action role-playing game set in an open world with a Viking setting.", 35, 10),
            ("Forza Horizon 4", "Racing game set in an open-world environment based on a fictional representation of the United Kingdom.", 40, 5),
            ("Grand Theft Auto V", "Action-adventure game with an open-world environment, played from a third-person perspective.", 50, 7),
            ("Xbox Series X", "Next-gen gaming console with powerful hardware and a vast library of games.", 300, 3),
            ("ASUS TUF Gaming F15 Laptop + DualShock 4 Wireless Controller Combo+ Headset", "Combo featuring a high-performance gaming laptop and an additional wireless controller with a headphone for gaming on the go.", 1800, 2),
            ("Logitech G Pro Gaming Mouse + Corsair K95 RGB Platinum XT Mechanical Keyboard Combo", "Combo featuring a high-performance gaming mouse and a premium mechanical keyboard.", 500, 8)
        ]
        cursor.executemany('''INSERT INTO devices (name, description, cost, stock)
                              VALUES (?, ?, ?, ?)''', devices)
        conn.commit()
        conn.close()

# Add initial devices to the table when the app starts
add_initial_devices()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    
    if user:
        # Redirect to some page upon successful login
        return redirect(url_for('terms_and_conditions'))
    else:
        # Redirect to login page with a message indicating invalid credentials
        error_message = "Invalid username or password."
        return redirect(url_for('login', error=error_message))

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        # Fetch data from the signup form
        first_name = request.form['name']
        last_name = request.form['lname']
        phone_number = request.form['phone']
        email = request.form['number']
        username = request.form['fusername']
        password = request.form['pass']
        
        # Insert user details into the SQLite database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (first_name, last_name, phone_number, email, username, password)
                          VALUES (?, ?, ?, ?, ?, ?)''', (first_name, last_name, phone_number, email, username, password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('t and c.html')

@app.route('/home')
def home():
    return render_template('Home1.html')


@app.route('/rent')
def rent():
    return render_template('rent.html')

@app.route('/pay/<int:device_id>')
def pay(device_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch the device details
    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    device = cursor.fetchone()

    if device:
        # Check if stock is available
        if device[4] > 0:
            # Decrement stock count by 1
            cursor.execute("UPDATE devices SET stock = stock - 1 WHERE id = ?", (device_id,))
            conn.commit()
            conn.close()
            return render_template('payment.html', device=device)
        else:
            # Redirect to a URL indicating that the stock is 0
            return redirect(url_for('out_of_stock', device_id=device_id))
    else:
        return "Device not found"

@app.route('/out_of_stock/<int:device_id>')
def out_of_stock(device_id):
    err1 = "Out of stock."
    return redirect(url_for('rent', error=err1))
@app.route('/thx')
def thx():
    return render_template('Thankyou.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
