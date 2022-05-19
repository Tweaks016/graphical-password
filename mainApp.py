"""
Graphical Password Authentication

"""
from flask import Flask, render_template, redirect, url_for, request, flash, session
from app import graphPassAuth
app = Flask(__name__)
app.secret_key = 'John The Ripper'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods = ['POST', 'GET'])
def registerNewUser():
    msg = None
    if request.method == 'POST':
        userName = request.form.get('username')
        name = request.form.get('name')
        userEmail = request.form.get('email')
        bool_val = graphPassAuth.registerUser(userName, name, userEmail)
        if bool_val == False:
            flash('Successfully registered')
            return redirect(url_for('home'))
        else:
            msg = 'Registration Failed'
            return redirect(url_for('registerNewUser'))
    return render_template('register.html', error=msg)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        bool_log_val = graphPassAuth.loginUser(email)
        if bool_log_val[0] == False:
            user = bool_log_val[1]
            session['loggedin'] = True
            session['user'] = user
            if user:
                return render_template('userPage.html', user=user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    return "Error"

@app.route('/login/logout', methods = ['POST'])
def logout():
    if request.method == 'POST':
        session.pop('loggedin', None)
        session.pop('user', None)
        print(session)
        print("LOUT")
        return redirect(url_for('home'))

# @app.route('/login/dashboard')
# def userHomePage(user):

if __name__ == '__main__':
    app.run(port=3000, debug=True)