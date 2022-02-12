from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
#import model that you need below
from flask_app.models import user
from flask_app.models import message


# CREATE CONTROLLERS
@app.route("/create_message", methods=["POST"])
def new_message():
    message.Message.create_message(request.form)
    return redirect("/dashboard")


#READ CONTROLLERS

#UPDATE CONTROLLERS

#DELETE CONTROLLERS
@app.route("/delete/<int:id>")
def delete_message(id):
    message.Message.delete_message(id)
    return redirect('/dashboard')