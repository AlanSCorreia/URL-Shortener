from os import path, makedirs, getcwd
import sqlite3

from flask import Flask, request, redirect


diretorio_atual = getcwd()
diretorio_db = path.join(diretorio_atual, "db")

if not path.exists(diretorio_db): makedirs(diretorio_db)


conexao = sqlite3.connect("db\\database.db", check_same_thread=False)
cursor = conexao.cursor()

with conexao:
    conexao.cursor().execute("""create table if not exists url (id integer,
                                        url_curta varchar(50) not null,
                                        url_redirecionada text not null,
                                        visualizacoes integer,
                                        PRIMARY KEY(id AUTOINCREMENT));""")
    

def cadastrar_url(url_curta, url_redirecionada, visualizacoes=0):

    cursor.execute("""INSERT INTO url (url_curta, url_redirecionada, visualizacoes)
                      VALUES (?, ?, ?);""", (url_curta, url_redirecionada, visualizacoes))
    conexao.commit()


def get_url(url_curta):
    cursor.execute("""SELECT url_redirecionada
                      FROM url
                      WHERE url_curta = ?;""", (url_curta,))
    retorno = cursor.fetchone()

    cursor.execute("""UPDATE url
                      SET visualizacoes = visualizacoes + 1
                      WHERE url_curta = ?;""", (url_curta,))
    conexao.commit()
        
    return retorno


app = Flask(__name__)


@app.route("/cadastrar")
def cadastrar_rota():
    received_data = request.get_json()
    cadastrar_url(*received_data.values())
    return "Criado", "201"


@app.route("/<url_short>")
def redirecionar_rota(url_short: str):
    url = get_url(url_short)[0]
    return redirect(url)


if __name__ == "__main__":
    app.run()
