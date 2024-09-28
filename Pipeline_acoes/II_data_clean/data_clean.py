import pandas as pd
import re
from unicodedata import normalize
from datetime import datetime


def format_column_names(text):
    # formatação dos nomes das colunas
    
    string_step1 = text.replace(".", "_")
    string_step2 = string_step1.replace(' ', "_")
    string_step3 = string_step2.replace('/', '_')
    string_step4 = string_step3.replace('__', '_')

    if '_' == string_step4[-1]:
        return normalize('NFKD', string_step4[:-1]).encode('ASCII', 'ignore').decode('ASCII')
    else:
        return normalize('NFKD', string_step4).encode('ASCII', 'ignore').decode('ASCII')


def main():
    
    # Leirura do arquivo
    data = pd.read_csv("../data/data.csv", sep=";")
    
    # Colocando os nomes das colunas em caixa alta 
    data.columns = data.columns.str.upper()
    
    # Identificando as colunas do DataFrame
    colunas_Df = data.columns
    
    columns_exclude = [
        'PAPEL',
        'DIV.YIELD',
        'MRG EBIT',
        'MRG. LÍQ.',
        'ROIC',
        'ROE',
        'CRESC. REC.5A',
    ]
    
    numerical_columns = list(data.columns)
    
    for i in columns_exclude:
        if i in numerical_columns:
            numerical_columns.remove(i)
    
    percentual_number_columns = [
        'DIV.YIELD',
        'MRG EBIT',
        'MRG. LÍQ.',
        'ROIC',
        'ROE',
        'CRESC. REC.5A'
    ]
    
    # transformando os valores percentuais para float
    for i in percentual_number_columns:
        data[i] = data[i].str[:-1]
        data[i] = data[i].str.replace(',', '.')
    
        for j in range(len(data[i])):
            list_index = []
            value = data[i][j]
    
            for index in range(len(value)):
                if value[index] == '.':
                    list_index.append(index)
    
            new_value = value[:list_index[-1]].replace('.', '') + value[list_index[-1]:]
            data.loc[j, i] = new_value
    
    for i in percentual_number_columns:
        data[i] = data[i].astype('float')
        data[i] = data[i]*0.01
    
    # transformando os dados numéricos em formato de String para tipo Float
    for i in numerical_columns:
        if data[i].dtype == 'object':
            data[i] = data[i].str.replace('.', '')
            data[i] = data[i].str.replace(',', '.')
            data[i] = data[i].astype('float')
    
    # preenchendo valores ausentes com Zero
    data.fillna(value=0, inplace=True)

    # Ajustes dos nomes das colunas

    columns = list(data.columns)
    new_columns = {col: format_column_names(col) for col in columns}
    data.rename(columns=new_columns, inplace=True)

    
    # salvando os dados em arquivo CSV

    data_atual = datetime.now().strftime('%Y_%m_%d')
    data.to_csv(f"../data/relatorio_acoes_{data_atual}.csv", index=False, sep=";")


if __name__ == "__main__":
    main()










