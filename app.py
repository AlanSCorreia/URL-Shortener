from os import path, makedirs, getcwd
import re
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


def obter_url(url_curta):
    cursor.execute("""SELECT url_redirecionada
                      FROM url
                      WHERE url_curta = ?;""", (url_curta,))
    retorno = cursor.fetchone()

    cursor.execute("""UPDATE url
                      SET visualizacoes = visualizacoes + 1
                      WHERE url_curta = ?;""", (url_curta,))
    conexao.commit()
        
    return retorno


def formatar_rota(url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    
    return "https://"+url


app = Flask(__name__)


@app.route("/cadastrar")
def cadastrar_rota():
    dados_recebidos = request.get_json()
    regex_url_valida = r'(https?://)?(www.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?'

    if re.match(regex_url_valida, dados_recebidos["url_redirecionada"]):
        url_curta = dados_recebidos["url_curta"]
        url_redirecionada = formatar_rota(dados_recebidos["url_redirecionada"])
        cadastrar_url(url_curta, url_redirecionada)
        return "Criado", "201"
    
    return "Falha no processo de cadastro", "400"


@app.route("/<url_curta>")
def redirecionar_rota(url_curta: str):
    url = obter_url(url_curta)[0]
    return redirect(url)


if __name__ == "__main__":
    app.run()
