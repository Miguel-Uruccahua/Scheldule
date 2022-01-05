

from flask import (
    Blueprint, g, render_template, request,flash, redirect, url_for, current_app
)
from mysql.connector.optionfiles import read_option_files
from app.db import get_db

from app.auth import  login, login_required

bp =Blueprint("contact",__name__,url_prefix="/")





@bp.route("/contact", methods=["GET"])
@login_required
def contact():
    db, c =get_db()
    c.execute(
        "SELECT * FROM contactos where id_user=%s ", 
        (g.user["id"], )
    )
    contactos = c.fetchall()
    return render_template("mails/contact.html", contactos=contactos)


@bp.route('/<int:id>/deletecontact', methods=["POST", "GET"])
@login_required
def deletecontact(id):
    db, c =get_db()
    c.execute(
        "DELETE FROM contactos where id=%s and id_user=%s ",
        (id, g.user["id"])
    )
    db.commit()
    return redirect(url_for("contact.contact"))



@bp.route('/<int:id>/editcontact', methods=["POST", "GET"])
@login_required
def editcontact(id):

    db, c =get_db()
    c.execute(
            "Select * from contactos where id= %s",
            (id, )
    )
    contacto=c.fetchone()

    if request.method == "POST":
        fullname=request.form.get("fullname")
        phone=request.form.get("phone")
        email=request.form.get("email")
        db, c =get_db()
        c.execute(
            "UPDATE contactos set fullname=%s, phone=%s, email=%s"
            " where id=%s and id_user=%s",
            (fullname, phone, email, id, g.user["id"] )
        )
        db.commit()

        return redirect(url_for("contact.contact"))
    else :
        return render_template("mails/editcontact.html", contacto=contacto )