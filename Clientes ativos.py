from imap_tools import MailBox, AND
import pandas as pd
import os
import re

username = "adm.happyenergy@gmail.com"
password = "mxtl agjv dcsn tcnv"
query = "Portal da Geração Distribuída: Solicitação"



mailbox = MailBox('imap.gmail.com').login(username, password)
lista_emails = mailbox.fetch(AND(from_='engenhariahappysolar@gmail.com', subject=query))

for email in lista_emails:
    print(email.subject)