from imap_tools import MailBox, AND

# pegar emails de um remetente para um destinatário
username = "adm.happyenergy@gmail.com"
password = "mxtl agjv dcsn tcnv"

# lista de imaps: https://www.systoolsgroup.com/imap/
meu_email = MailBox('imap.gmail.com').login(username, password)

# criterios: https://github.com/ikvk/imap_tools#search-criteria
lista_emails = meu_email.fetch(AND(from_="assistencia.happyenergy@gmail.com")) 
for email in lista_emails:
    print(email.subject)
    print(email.text)


# pegar emails com um anexo específico
lista_emails = meu_email.fetch(AND(from_="assistencia.happyenergy@gmail.com"))
for email in lista_emails:
    if len(email.attachments) > 0:
        for anexo in email.attachments:
            if "RelatorioResumo" in anexo.filename:
                # print(anexo.content_type)
                # print(anexo.payload)
                with open("RelatorioResumo.pdf", 'wb') as arquivo_excel:
                    arquivo_excel.write(anexo.payload)