from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'assdasddasdakdgasjhdsajdgashjgdiasudgueidgasiudgiagdsaiud'
conn = sqlite3.connect('auth.db')
conn.execute("""
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT,
             role TEXT)
            """)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        db = sqlite3.connect('auth.db')
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, password)).fetchone()
        if user is None:
            return render_template('login.html', error='Wrong credentials')
        else:
            session.clear()
            session['username'] = username
            session['role'] = user[3]
            if user[3] == 'user':
                return redirect('/profile')
            elif user[3] == 'admin':
                return redirect('/dashboard')
            else:
                return render_template('login.html', error='Unknown role')
    else:
        return render_template('login.html')


@app.route("/register")
def register():
    pass


@app.route("/profile")
def profile():
    if (session.get('role') is None) or (session.get('role') != 'user'):
        return render_template('login.html', error='No access')
    
    return render_template('profile.html')


@app.route("/dashboard")
def dashboard():
    if (session.get('role') is None) or (session.get('role') != 'admin'):
        return render_template('login.html', error='No access')
    return render_template('dashboard.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
