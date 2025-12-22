import pdfplumber
import pandas as pd

def extrair_dados_neoenergia(caminho_pdf):
    dados_extraidos = {}

    with pdfplumber.open(caminho_pdf) as pdf:
        # 1. Extração de texto geral (Cliente e Período)
        primeira_pagina = pdf.pages[0].extract_text()
        # Aqui você usaria Regex para buscar o nome após "Cliente:"
        
        # 2. Extração de Tabelas
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())

        # Tabela de Injetados (Geralmente a primeira com 'Descrição' e 'Gerador')
        # Baseado no 
        df_gerador = pd.DataFrame(tables[0][1:], columns=tables[0][0])
        
        # Tabela de Consumo
        # Baseado no 
        df_consumo = pd.DataFrame(tables[1][1:], columns=tables[1][0])

        # Tabela de Histórico (SITUAÇÃO MENSAL)
        # Baseado no 
        for table in tables:
            if "SITUAÇÃO" in str(table[0]):
                df_historico = pd.DataFrame(table[1:], columns=table[0])
                dados_extraidos['historico'] = df_historico

        # Resumo do Saldo de Crédito
        # Baseado no 
        for table in tables:
            # Adicione prints para depurar
            print(f"Cabeçalhos da tabela: {table[0]}")  # Remova após depuração
            if "CÓDIGO DO CLIENTE" in str(table[0]) and "% DE COMPENSAÇÃO" in str(table[0]):
                df_saldo = pd.DataFrame(table[1:], columns=table[0])
                dados_extraidos['saldo_unidades'] = df_saldo

    return dados_extraidos

# Uso
resultado = extrair_dados_neoenergia("RelatorioResumo.pdf")
if 'saldo_unidades' in resultado:
    print(resultado['saldo_unidades'])
else:
    print("Tabela de saldo não encontrada. Verifique os cabeçalhos das tabelas.")