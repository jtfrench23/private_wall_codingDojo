from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
#import model that you need below
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
# CREATE
@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    hashed_password=bcrypt.generate_password_hash(request.form['password'])
    print(hashed_password)
    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_password
    }
    user_id= user.User.save(data)
    session['user_id']=user_id
    session['user_email']=request.form['email']
    session['user_name']=request.form['first_name']
    return redirect('/dashboard')


#READ
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    if "count" not in session:
        session["count"]=0
    person= user.User.get_by_email(session['user_email'])
    all_users= user.User.get_all()
    message_count=len(person.messages)
    print(person)
    return render_template("dashboard.html", user=person, all_users=all_users, message_count=message_count)

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    user_in_db = user.User.get_by_email(request.form['email'])
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['user_name']= user_in_db.first_name
    session['user_email']=user_in_db.email
    # never render on a post!!!
    return redirect("/dashboard")
@app.route('/danger')
def danger():
    session['count']+=1
    if session['count']==2:
        return redirect('/logout')
    ip_addr = request.remote_addr
    return render_template('danger.html', ip_addr=ip_addr) 


#UPDATE


#DELETE
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")