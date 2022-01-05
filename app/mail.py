

from flask import (
    Blueprint, g, render_template, request,flash, redirect, url_for, current_app
)
from werkzeug.security import generate_password_hash
from app.db import get_db
import sendgrid
from sendgrid.helpers.mail import *

from app.auth import  login_required

bp =Blueprint("mail",__name__,url_prefix="/")


@bp.route("/", methods=["GET"])
@login_required
def index():
    search=request.args.get("search")
    db, c =get_db()
    if search is None:
        c.execute(
            "SELECT e.id, e.from_email, e.email, e.subject, e.content "
           " FROM email e JOIN  user u on e.from_email=u.id where u.id=%s ",
            (g.user["id"], )
        )
    else:
        c.execute(
            "SELECT * FROM email WHERE content like %s and from_email= %s ",
            ("%" + search + "%", g.user["id"])
        )
    mails =c.fetchall()

    return render_template("mails/index.html", mails=mails)


@bp.route("/create", methods=["GET","POST"])
@login_required
def create():
    if request.method=="POST":
        email=request.form.get("email")
        subject=request.form.get("subject")
        content=request.form.get("content")
        errors=[]
        if not email:
            errors.append("email es obligatorio")
        if not subject:
            errors.append("email es obligatorio")      
        if not content:
            errors.append("email es obligatorio")
        if len(errors)==0:
            send(email, subject, content)
            db, c = get_db()
            c.execute(
                "INSERT INTO email (from_email, email, subject, content) VALUES (%s, %s, %s, %s)", 
                (g.user["id"], email, subject, content)
            )
            db.commit()
            
            return redirect(url_for("mail.index"))
        else:
            for error in errors:
                flash(error)

    return render_template("mails/create.html")

def send(to, subject, content):
    sg= sendgrid.SendGridAPIClient(api_key = current_app.config["SENDGRID_KEY"])
    from_email = Email(current_app.config["FROM_EMAIL"]) 
    to_email=To(to)
    content =Content("text/plain", content)
    mail=Mail(from_email, to_email, subject, content)
    response=sg.client.mail.send.post(request_body=mail.get())
    print(response)

@bp.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method=="POST":
        fullname=request.form.get("fullname")
        phone=request.form.get("phone")
        email=request.form.get("email")
        error_add=[]
        if not fullname:
            error_add.append("email es obligatorio")
        if not phone:
            error_add.append("email es obligatorio")      
        if not email:
            error_add.append("email es obligatorio")
        if len(error_add)==0:
            db, c = get_db()
            c.execute(
                "INSERT INTO contactos (id_user, fullname, phone, email) VALUES (%s,%s, %s, %s)",
                (g.user["id"], fullname, phone, email)
            )
            db.commit()

            return redirect(url_for("contact.contact"))
        else:
            for error in error_add:
                flash(error)

    return render_template("mails/add.html")

@bp.route("/changepassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method== "POST":
        new_password=request.form.get("nuevoPassword")
        confirmation_password=request.form.get("confirmacionPassword")
        if new_password == confirmation_password : 
            db, c = get_db()
            c.execute(
                "UPDATE user set password= %s where id = %s",
                (generate_password_hash(new_password), g.user["id"])
            )
            db.commit()
            return redirect(url_for("mail.index"))
        else:
            flash("Las contraseñas no coinciden","warning")
            return render_template("mails/changePassword.html")
    else:
        return render_template("mails/changePassword.html")
