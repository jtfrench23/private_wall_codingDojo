from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
#import model that you need below
from flask_app.models import user
# CREATE
@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    return redirect('/dashboard')


#READ
@app.route("/")
def index():
    
    return render_template("index.html")

#UPDATE


#DELETE
