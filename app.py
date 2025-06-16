from flask import Flask, request, redirect
import sqlite3


context = sqlite3.connect("db\\database.db", check_same_thread=False)
cursor = context.cursor()

with context:
    context.cursor().execute("""create table if not exists url (id integer,
                                        url_short varchar(50) not null,
                                        url_redirect text not null,
                                        PRIMARY KEY(id AUTOINCREMENT));""")
    

def cadastrar_url(url_short, url_redirect):

    cursor.execute("""INSERT INTO url (url_short, url_redirect) VALUES
                                (?, ?);""", (url_short, url_redirect))
    context.commit()


def get_url(url_short):
    cursor.execute("""SELECT url_redirect
                                FROM url
                                WHERE url_short = ?;""", (url_short,))
        
    return cursor.fetchone()


app = Flask(__name__)


@app.route("/cadastrar")
def index():
    received_data = request.get_json()
    cadastrar_url(*received_data.values())
    return "Criado", "201"


@app.route("/<url_short>")
def redirecionar_rota(url_short: str):
    url = get_url(url_short)[0]
    return redirect(url)


if __name__ == "__main__":
    app.run()
