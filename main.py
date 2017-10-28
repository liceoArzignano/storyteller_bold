from flask import Flask, render_template, flash, request
from news import News
from wtforms import Form, validators, StringField, PasswordField
import firebase
import time


class ReusableForm(Form):
    username = StringField("Username:", validators=[validators.required()])
    password = PasswordField("Password:", validators=[validators.required()])

    title = StringField("Title:", validators=[validators.required()])
    message = StringField("Message:", validators=[validators.required()])
    url = StringField("Url:", validators=[validators.URL])


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '74d41f27d661f11567a4abf2b6176a'


@app.route("/", methods=["GET", "POST"])
def storyteller():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == "POST":
        username = request.form["username"]
        password = str(request.form["password"])

        if form.validate():
            auth = firebase.database_auth(username, password)

            if auth == 0:
                news = News()
                news.title = request.form["title"]
                news.message = request.form["message"]
                news.url = request.form["url"]
                news.date = time.strftime("%Y-%m-%d")
                news.is_private = False

                firebase.fcm(news, True)
                flash("Messaggio inviato con successo")
            elif auth == 1:
                flash("Errore: chiave API non definita")
            elif auth == 2:
                flash("Errore: nome utente non riconosciuto")
            elif auth == 3:
                flash("Errore: nome utente o password errata")
        else:
            flash("Errore: compila tutti i campi")

    return render_template("storyteller.html", form=form)


if __name__ == "__main__":
    app.run()
