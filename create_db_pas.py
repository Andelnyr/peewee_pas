import sys
import csv
from os import walk


def gerar_listname(dir_name):  # NOQA
    """Gera lista com nomes dos arquivos existentes em dir_name."""
    listname = []  # NOQA
    for dName, sdName, fList in walk(dir_name):
        for fileName in fList:
            listname.append("/".join([dName, fileName]))
    return listname


if __name__ == '__main__':

    # Lendo nome do diretório onde estão os arquivos csv
    if len(sys.argv) == 2:
        _, dir_name = sys.argv
        ids_csv = None

    # Gerando lista com os nomes dos arquivos csv
    listname = gerar_listname(dir_name)  # NOQA
    arqs_csv = [arq for arq in listname if '.csv' in arq]
    arqs_csv = sorted(arqs_csv)

    # Processando cada arquivo csv
    colunas_total = []
    valores_total = []
    for arq_csv in arqs_csv:
        print(f'\nProcessando: {arq_csv}')

        with open(arq_csv) as csv_file:
            # Capturando os nomes das colunas
            csv_reader = csv.reader(csv_file, delimiter=';')
            csv_reader = list(csv_reader)
            colunas = [coluna.replace('\\', '_').replace('/', '_').replace('-', '_').replace('.', '_')
                       for coluna in csv_reader[0]]
            colunas_total = colunas_total + colunas

            # Formando um dicionário com os nomes das colunas corrigidos
            for lista in csv_reader[1:]:
                valores = dict(zip(colunas, lista))
                valores_total.append(valores)

    # Processando todas as colunas para formar uma lista unique de nomes de
    # colunas em ordem alfabética começando por "TIMESTAMP, DIA_SEM"]
    colunas_total = [coluna for coluna in set(colunas_total) if coluna not in ['TIMESTAMP', 'DIA_SEM']]
    colunas_total = ['TIMESTAMP', 'DIA_SEM'] + sorted(colunas_total)

    with open('criar_tabela.py', 'w') as arquivo:
        arquivo.write('from peewee import SqliteDatabase, Model, TextField\n')
        arquivo.write('\n')
        arquivo.write("db = SqliteDatabase('base_pas.db')\n")
        arquivo.write('\n')
        arquivo.write('class BaseModel(Model):\n')
        arquivo.write('    class Meta:\n')
        arquivo.write('        database = db\n')
        arquivo.write('\n')
        arquivo.write('class Valores(BaseModel):\n')

        for coluna in colunas_total:
            arquivo.write(f'    {coluna} = TextField()\n')

        arquivo.write('\n')
        arquivo.write('Valores.create_table()\n')
        arquivo.write('\n')


    from criar_tabela import Valores
    
    for valores in valores_total:
        Valores.insert_many(valores).execute()



