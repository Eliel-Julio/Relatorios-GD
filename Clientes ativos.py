from imap_tools import MailBox, AND
import pandas as pd
import os
import re

# username = "adm.happyenergy@gmail.com"
# password = "mxtl agjv dcsn tcnv" #adm.happyenergy@gmail.com
# _from = "engenhariahappysolar@gmail.com"

username = "engenhariahappysolar@gmail.com"
password = "jtpg hdvr pmat rtap" #engenhariahappysolar@gmail.com
_from = 'noreplyportalgd@neoenergia.com'

query = "Portal da Geração Distribuída: Solicitação "


mailbox = MailBox('imap.gmail.com').login(username, password)
lista_emails = mailbox.fetch(AND(from_=_from))
lista_emails_com_query = [email for email in lista_emails if query.lower() in email.subject.lower()]
print("Emails encontrados:", len(list(lista_emails)))

for email in lista_emails:
    print(email.subject)
    print(email.date)

# Modificação para extrair número da solicitação e nome do cliente
dados_clientes = []

for email in lista_emails_com_query:
    # Extrair número da solicitação do assunto (assumindo formato "Solicitação XXXX")
    match_num = re.search(r'Solicitação (\d+)', email.subject)
    numero_solicitacao = match_num.group(1) if match_num else "Não encontrado"
    
    # Extrair nome do cliente do corpo do email (assumindo que está em uma linha como "Cliente: Nome")
    # Você pode ajustar o regex conforme o formato exato do email
    match_nome = re.search(r'Prezado\(a\)\s+(.+?),', email.text, re.IGNORECASE)
    nome_cliente = match_nome.group(1).strip() if match_nome else "Não encontrado"  
    
    dados_clientes.append({
        'numero_solicitacao': numero_solicitacao,
        'nome_cliente': nome_cliente,
        'data': email.date
    })
    # print(f"Extraído - Solicitação: {numero_solicitacao}, Cliente: {nome_cliente}")
    print(email.text)

# Criar DataFrame e salvar em CSV
df = pd.DataFrame(dados_clientes)
df.to_csv('clientes_ativos.csv', index=False)
print("Lista gerada e salva em clientes_ativos.csv")
print(df)