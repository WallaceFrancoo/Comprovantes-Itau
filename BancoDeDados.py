import sqlite3
import datetime
import parametros
from tkinter import messagebox

conn = sqlite3.connect(parametros.caminhobancodedados)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dePara (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    DE TEXT NOT NULL,
    PARA TEXT NOT NULL
)
''')

def consultarHistorico(valor):
    cursor.execute('SELECT * FROM dePara')
    tabelaHistorico = cursor.fetchall()

    if tabelaHistorico:
        cursor.execute('SELECT DE, PARA FROM dePara WHERE ? LIKE "%" || DE || "%" COLLATE NOCASE', (valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][1]
        else:
            return f"6"
    else:
        return f"6"