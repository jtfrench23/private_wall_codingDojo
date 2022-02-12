from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
#import model that you need below
from flask_app.models import user
from flask_app.models import message


# CREATE CONTROLLERS
@app.route("/create_message", methods=["POST"])
def new_message():
    if not message.Message.validate_message(request.form):
        # we redirect to the template with the form.
        return redirect('/dashboard')
    message.Message.create_message(request.form)
    return redirect("/dashboard")


#READ CONTROLLERS

#UPDATE CONTROLLERS

#DELETE CONTROLLERS
@app.route("/delete/<int:id>")
def delete_message(id):
    message_id=id
    if not message.Message.validate_delete(message_id, session['user_id']):
        return redirect('/danger')
    message.Message.delete_message(id)
    return redirect('/dashboard')