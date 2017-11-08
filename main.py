from flask import Flask, render_template, flash, request
from news import News
from wtforms import Form, validators, StringField, PasswordField
import firebase
import time


class ReusableForm(Form):
    email = StringField("Email:", validators=[validators.required(), validators.email()])
    password = PasswordField("Password:", validators=[validators.required()])

    title = StringField("Title:", validators=[validators.required()])
    message = StringField("Message:", validators=[validators.required()])
    url = StringField("Url:", validators=[validators.URL])


def message_with_signature(message: str, email: str):
    user = email.split("@")[0]
    return message + "\nInviato da " + user + "."


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '74d41f27d661f11567a4abf2b6176a'


@app.route("/", methods=["GET", "POST"])
def storyteller():
    form = ReusableForm(request.form)

    if request.method == "POST":
        if form.validate():
            email = request.form["email"]
            password = str(request.form["password"])
            login = firebase.login(email, password)

            if login == 0:
                news = News()
                news.title = request.form["title"]
                news.message = message_with_signature(request.form["message"], email)
                news.url = request.form["url"]
                news.date = time.strftime("%Y-%m-%d")
                news.is_private = False

                firebase.fcm(news, True)
                print(news.message)
                flash("Messaggio inviato con successo")
            if login == 1:
                flash("Errore: nome utente o password errata")
            elif login == 2:
                flash("Errore: chiave API non definita")
            elif login == 3:
                flash("Errore: account non valido")
        else:
            flash("Compila tutti i campi")

    return render_template("storyteller.html", form=form)


if __name__ == "__main__":
    app.run()
